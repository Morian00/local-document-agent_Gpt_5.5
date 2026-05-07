from __future__ import annotations

import argparse
import asyncio
import json
import sys
from dataclasses import dataclass
from typing import Any

from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamable_http_client


TINY_PNG_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


@dataclass(frozen=True)
class SmokeCall:
    name: str
    arguments: dict[str, Any]


def _core_calls() -> list[SmokeCall]:
    return [
        SmokeCall("ping", {}),
        SmokeCall("list_files", {"path": ".", "recursive": True}),
        SmokeCall(
            "write_text_file",
            {
                "path": "docs/smoke-batch.md",
                "content": "# Batch Smoke\n\n상태: before\n",
                "overwrite": True,
                "create_backup": True,
            },
        ),
        SmokeCall("read_text_file", {"path": "docs/smoke-batch.md", "max_chars": 2000}),
        SmokeCall(
            "patch_text_file",
            {
                "path": "docs/smoke-batch.md",
                "replacements": [
                    {"find": "상태: before", "replace": "상태: after", "must_match_once": True},
                ],
                "create_backup": True,
            },
        ),
        SmokeCall(
            "create_markdown",
            {
                "path": "docs/smoke-structured.md",
                "title": "배치 검증 문서",
                "summary": "MCP 도구 일괄 호출 검증용 문서.",
                "sections": [
                    {"heading": "범위", "body": "- Markdown\n- DOCX\n- XLSX\n- PPTX"},
                    {"heading": "판정", "body": "배치 스모크 검증 대상."},
                ],
                "overwrite": True,
                "create_backup": True,
            },
        ),
        SmokeCall(
            "export_docx_from_markdown",
            {
                "source_path": "docs/smoke-structured.md",
                "output_path": "output/smoke-structured.docx",
                "overwrite": True,
                "create_backup": True,
            },
        ),
        SmokeCall(
            "extract_docx_text",
            {
                "source_path": "output/smoke-structured.docx",
                "max_chars": 2000,
                "include_paragraphs": True,
            },
        ),
        SmokeCall(
            "create_xlsx_from_sheets",
            {
                "output_path": "output/smoke-checklist.xlsx",
                "sheets": [
                    {
                        "name": "Checklist",
                        "headers": ["항목", "담당", "상태"],
                        "rows": [
                            ["DOCX", "Planner", "완료"],
                            ["XLSX", "Planner", "완료"],
                            ["PPTX", "Planner", "완료"],
                        ],
                    }
                ],
                "overwrite": True,
                "create_backup": True,
            },
        ),
        SmokeCall(
            "extract_xlsx_text",
            {
                "source_path": "output/smoke-checklist.xlsx",
                "query": "완료",
                "max_cells": 200,
                "max_chars": 4000,
            },
        ),
        SmokeCall(
            "create_pptx_from_spec",
            {
                "output_path": "output/smoke-deck.pptx",
                "title": "Local Document Agent",
                "subtitle": "Batch Smoke",
                "slides": [
                    {
                        "title": "검증 범위",
                        "bullets": ["Markdown", "DOCX", "XLSX", "PPTX"],
                    },
                    {
                        "title": "후속 작업",
                        "body": "ChatGPT UI 검증은 모드 제약을 별도 기록한다.",
                    },
                ],
                "overwrite": True,
                "create_backup": True,
            },
        ),
        SmokeCall(
            "save_base64_image",
            {
                "output_path": "assets/smoke-pixel.png",
                "image_base64": TINY_PNG_BASE64,
                "overwrite": True,
                "create_backup": True,
            },
        ),
        SmokeCall("list_assets", {"path": "assets", "recursive": True}),
        SmokeCall(
            "insert_image_to_markdown",
            {
                "markdown_path": "docs/smoke-structured.md",
                "image_path": "assets/smoke-pixel.png",
                "alt_text": "Smoke pixel",
                "position": "append",
                "create_backup": True,
            },
        ),
        SmokeCall(
            "insert_image_to_pptx",
            {
                "pptx_path": "output/smoke-deck.pptx",
                "image_path": "assets/smoke-pixel.png",
                "slide_index": 1,
                "left": 8.0,
                "top": 1.5,
                "width": 1.0,
                "create_backup": True,
            },
        ),
        SmokeCall("list_templates", {}),
        SmokeCall(
            "create_markdown_from_template",
            {
                "template_name": "planning_doc",
                "output_path": "docs/smoke-template.md",
                "title": "배치 템플릿 검증",
                "summary": "템플릿 기반 Markdown 생성 검증.",
                "overwrite": True,
                "create_backup": True,
            },
        ),
        SmokeCall(
            "create_docx_from_template",
            {
                "template_name": "proposal_doc",
                "output_path": "output/smoke-template.docx",
                "title": "배치 템플릿 제안서",
                "summary": "템플릿 기반 DOCX 생성 검증.",
                "overwrite": True,
                "create_backup": True,
            },
        ),
        SmokeCall(
            "create_pptx_from_template",
            {
                "template_name": "planning_doc",
                "output_path": "output/smoke-template.pptx",
                "title": "배치 템플릿 발표자료",
                "summary": "템플릿 기반 PPTX 생성 검증.",
                "overwrite": True,
                "create_backup": True,
            },
        ),
    ]


def _extract_payload(result: Any) -> dict[str, Any]:
    if getattr(result, "structuredContent", None):
        structured = result.structuredContent
        if isinstance(structured, dict):
            return structured

    content = getattr(result, "content", None) or []
    if not content:
        return {"ok": False, "error": "tool returned no content"}

    first = content[0]
    text = getattr(first, "text", None)
    if text is None:
        return {"ok": False, "error": f"tool returned unsupported content: {type(first).__name__}"}

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return {"ok": False, "error": "tool returned non-JSON text", "text": text}

    if isinstance(payload, dict):
        return payload
    return {"ok": False, "error": "tool returned non-object JSON", "payload": payload}


async def _run_smoke(url: str) -> tuple[bool, list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []

    async with streamable_http_client(url) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            listed = await session.list_tools()
            available = {tool.name for tool in listed.tools}

            for call in _core_calls():
                if call.name not in available:
                    rows.append({"tool": call.name, "ok": False, "error": "tool is not listed by server"})
                    continue

                try:
                    result = await session.call_tool(call.name, call.arguments)
                    payload = _extract_payload(result)
                except Exception as exc:
                    rows.append({"tool": call.name, "ok": False, "error": str(exc)})
                    continue

                rows.append(
                    {
                        "tool": call.name,
                        "ok": bool(payload.get("ok")),
                        "path": payload.get("path") or payload.get("output_path"),
                        "error": payload.get("error"),
                    }
                )

    return all(row["ok"] for row in rows), rows


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a batch MCP smoke test against a streamable HTTP endpoint.",
    )
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:2091/mcp",
        help="MCP streamable HTTP endpoint URL.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    ok, rows = asyncio.run(_run_smoke(args.url))
    summary = {
        "ok": ok,
        "url": args.url,
        "passed": sum(1 for row in rows if row["ok"]),
        "failed": sum(1 for row in rows if not row["ok"]),
        "results": rows,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
