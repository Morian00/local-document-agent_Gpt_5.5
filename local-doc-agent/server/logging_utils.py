from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from .config import settings


def write_operation_log(tool_name: str, result: dict[str, Any]) -> None:
    settings.logs_root.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": tool_name,
        "ok": result.get("ok", False),
        "path": result.get("path"),
        "source_path": result.get("source_path"),
        "output_path": result.get("output_path"),
        "backup_path": result.get("backup_path"),
        "created": result.get("created"),
        "changed_count": result.get("changed_count"),
        "diff_summary": result.get("diff_summary"),
        "error": result.get("error"),
    }
    with settings.operations_log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
