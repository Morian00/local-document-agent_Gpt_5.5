from __future__ import annotations

import difflib
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import ensure_base_directories, settings
from .logging_utils import write_operation_log


TEXT_EXTENSIONS = {".md", ".txt", ".json", ".csv", ".yaml", ".yml"}
DEFAULT_LIST_EXTENSIONS = [".md", ".txt", ".docx", ".pptx", ".xlsx", ".png", ".jpg", ".jpeg", ".webp"]


def _to_workspace_relative(path: Path) -> str:
    return path.resolve().relative_to(settings.workspace_root).as_posix()


def _resolve_workspace_path(path: str | None) -> Path:
    raw = "." if path is None or path == "" else path
    candidate = (settings.workspace_root / raw).resolve()
    try:
        candidate.relative_to(settings.workspace_root)
    except ValueError as exc:
        raise ValueError(f"workspace 밖의 경로는 사용할 수 없음: {path}") from exc
    return candidate


def _ensure_text_extension(path: Path) -> None:
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        allowed = ", ".join(sorted(TEXT_EXTENSIONS))
        raise ValueError(f"텍스트 도구는 다음 확장자만 지원함: {allowed}")


def _diff_summary(before: str, after: str) -> dict[str, int]:
    before_lines = before.splitlines(keepends=True)
    after_lines = after.splitlines(keepends=True)
    diff = difflib.unified_diff(before_lines, after_lines, lineterm="")
    added = 0
    removed = 0
    for line in diff:
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+"):
            added += 1
        elif line.startswith("-"):
            removed += 1
    return {"added_lines": added, "removed_lines": removed}


def _backup_existing_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None

    relative = path.relative_to(settings.workspace_root)
    backup_dir = settings.backups_root / relative.parent
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_name = f"{path.stem}.{timestamp}{path.suffix}"
    backup_path = backup_dir / backup_name

    counter = 1
    while backup_path.exists():
        backup_path = backup_dir / f"{path.stem}.{timestamp}-{counter}{path.suffix}"
        counter += 1

    shutil.copy2(path, backup_path)
    return _to_workspace_relative(backup_path)


def _safe_result(tool_name: str, action: Any) -> dict[str, Any]:
    try:
        ensure_base_directories()
        result = action()
    except Exception as exc:  # Tool boundaries should return readable errors to ChatGPT.
        result = {"ok": False, "error": str(exc)}
    write_operation_log(tool_name, result)
    return result


def ping_tool() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        return {
            "ok": True,
            "server": "local-doc-agent",
            "workspace": str(settings.workspace_root),
            "mcp_path": "/mcp",
        }

    return _safe_result("ping", action)


def list_files_tool(
    path: str = ".",
    recursive: bool = True,
    extensions: list[str] | None = None,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        root = _resolve_workspace_path(path)
        if not root.exists():
            return {"ok": True, "root": str(settings.workspace_root), "files": []}

        selected_extensions = extensions or DEFAULT_LIST_EXTENSIONS
        normalized_extensions = {item.lower() for item in selected_extensions}

        candidates: list[Path]
        if root.is_file():
            candidates = [root]
        elif recursive:
            candidates = [item for item in root.rglob("*") if item.is_file()]
        else:
            candidates = [item for item in root.iterdir() if item.is_file()]

        files = [
            _to_workspace_relative(item)
            for item in sorted(candidates)
            if not normalized_extensions or item.suffix.lower() in normalized_extensions
        ]
        return {"ok": True, "root": str(settings.workspace_root), "files": files}

    return _safe_result("list_files", action)


def read_text_file_tool(path: str, max_chars: int | None = None) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        target = _resolve_workspace_path(path)
        _ensure_text_extension(target)
        if not target.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없음: {path}")
        if not target.is_file():
            raise ValueError(f"파일이 아님: {path}")

        limit = max_chars or settings.max_read_chars
        content = target.read_text(encoding="utf-8")
        truncated = len(content) > limit
        if truncated:
            content = content[:limit]
        return {
            "ok": True,
            "path": _to_workspace_relative(target),
            "content": content,
            "truncated": truncated,
        }

    return _safe_result("read_text_file", action)


def write_text_file_tool(
    path: str,
    content: str,
    overwrite: bool | None = None,
    create_backup: bool | None = None,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        target = _resolve_workspace_path(path)
        _ensure_text_extension(target)

        should_overwrite = settings.default_overwrite if overwrite is None else overwrite
        should_backup = settings.create_backup if create_backup is None else create_backup

        exists = target.exists()
        if exists and not should_overwrite:
            raise FileExistsError(f"파일이 이미 존재함: {path}")
        if exists and not target.is_file():
            raise ValueError(f"파일이 아님: {path}")

        before = target.read_text(encoding="utf-8") if exists else ""
        backup_path = _backup_existing_file(target) if exists and should_backup else None

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")

        return {
            "ok": True,
            "path": _to_workspace_relative(target),
            "created": not exists,
            "backup_path": backup_path,
            "diff_summary": _diff_summary(before, content),
        }

    return _safe_result("write_text_file", action)


def patch_text_file_tool(
    path: str,
    replacements: list[dict[str, Any]],
    create_backup: bool | None = None,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        target = _resolve_workspace_path(path)
        _ensure_text_extension(target)
        if not target.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없음: {path}")
        if not target.is_file():
            raise ValueError(f"파일이 아님: {path}")

        before = target.read_text(encoding="utf-8")
        after = before
        changed_count = 0

        for replacement in replacements:
            find = str(replacement.get("find", ""))
            replace = str(replacement.get("replace", ""))
            must_match_once = bool(replacement.get("must_match_once", False))

            if find == "":
                raise ValueError("find 값은 비어 있을 수 없음")

            occurrences = after.count(find)
            if must_match_once and occurrences != 1:
                raise ValueError(f"must_match_once 실패: '{find}' 발견 횟수 {occurrences}")
            if occurrences == 0:
                continue

            after = after.replace(find, replace)
            changed_count += occurrences

        should_backup = settings.create_backup if create_backup is None else create_backup
        backup_path = _backup_existing_file(target) if changed_count > 0 and should_backup else None

        if changed_count > 0:
            target.write_text(after, encoding="utf-8", newline="\n")

        return {
            "ok": True,
            "path": _to_workspace_relative(target),
            "backup_path": backup_path,
            "changed_count": changed_count,
            "diff_summary": _diff_summary(before, after),
        }

    return _safe_result("patch_text_file", action)
