from __future__ import annotations

import re
from typing import Any


SUSPICIOUS_QUESTION_MARKS = re.compile(r"\?{2,}")


def reject_suspicious_question_marks(value: Any, *, label: str = "input") -> None:
    if value is None:
        return

    if isinstance(value, str):
        if SUSPICIOUS_QUESTION_MARKS.search(value):
            raise ValueError(
                f"{label} 값에 인코딩 손상으로 보이는 연속 물음표가 포함됨. "
                "원문 한글을 복구한 뒤 다시 요청 필요."
            )
        return

    if isinstance(value, dict):
        for key, item in value.items():
            reject_suspicious_question_marks(item, label=f"{label}.{key}")
        return

    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            reject_suspicious_question_marks(item, label=f"{label}[{index}]")
