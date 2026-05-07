from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover - dependency is installed via uv.
    load_dotenv = None


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if load_dotenv is not None:
    load_dotenv(PROJECT_ROOT / ".env")


def _bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _path_env(name: str, default: str) -> Path:
    raw = os.getenv(name, default)
    path = Path(raw)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path.resolve()


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    workspace_root: Path
    logs_root: Path
    default_overwrite: bool
    create_backup: bool
    max_read_chars: int

    @property
    def backups_root(self) -> Path:
        return self.workspace_root / "backups"

    @property
    def operations_log_path(self) -> Path:
        return self.logs_root / "operations.jsonl"


settings = Settings(
    host=os.getenv("LOCAL_DOC_AGENT_HOST", "127.0.0.1"),
    port=int(os.getenv("LOCAL_DOC_AGENT_PORT", "2091")),
    workspace_root=_path_env("LOCAL_DOC_AGENT_WORKSPACE", "workspace"),
    logs_root=_path_env("LOCAL_DOC_AGENT_LOGS", "logs"),
    default_overwrite=_bool_env("LOCAL_DOC_AGENT_DEFAULT_OVERWRITE", True),
    create_backup=_bool_env("LOCAL_DOC_AGENT_CREATE_BACKUP", True),
    max_read_chars=int(os.getenv("LOCAL_DOC_AGENT_MAX_READ_CHARS", "50000")),
)


def ensure_base_directories() -> None:
    for path in [
        settings.workspace_root,
        settings.workspace_root / "docs",
        settings.workspace_root / "assets",
        settings.workspace_root / "output",
        settings.backups_root,
        settings.logs_root,
    ]:
        path.mkdir(parents=True, exist_ok=True)
