from __future__ import annotations

import importlib


def _reload_modules(monkeypatch, tmp_path):
    monkeypatch.setenv("LOCAL_DOC_AGENT_WORKSPACE", str(tmp_path / "workspace"))
    monkeypatch.setenv("LOCAL_DOC_AGENT_LOGS", str(tmp_path / "logs"))

    import server.config as config
    import server.logging_utils as logging_utils
    import server.tools_files as tools_files

    importlib.reload(config)
    importlib.reload(logging_utils)
    importlib.reload(tools_files)
    return tools_files, config.settings


def test_write_read_and_patch_text_file(monkeypatch, tmp_path):
    tools, settings = _reload_modules(monkeypatch, tmp_path)

    written = tools.write_text_file_tool("docs/test.md", "# Test\n\nOld text\n")
    assert written["ok"] is True
    assert written["created"] is True

    read = tools.read_text_file_tool("docs/test.md")
    assert read["ok"] is True
    assert "Old text" in read["content"]

    patched = tools.patch_text_file_tool(
        "docs/test.md",
        [{"find": "Old text", "replace": "New text", "must_match_once": True}],
    )
    assert patched["ok"] is True
    assert patched["changed_count"] == 1
    assert patched["backup_path"] is not None

    updated = (settings.workspace_root / "docs" / "test.md").read_text(encoding="utf-8")
    assert "New text" in updated


def test_list_files_filters_extensions(monkeypatch, tmp_path):
    tools, _settings = _reload_modules(monkeypatch, tmp_path)

    tools.write_text_file_tool("docs/a.md", "A")
    tools.write_text_file_tool("docs/b.txt", "B")

    listed = tools.list_files_tool(".", recursive=True, extensions=[".md"])
    assert listed["ok"] is True
    assert listed["files"] == ["docs/a.md"]
