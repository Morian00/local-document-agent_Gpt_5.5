from __future__ import annotations

import importlib


def _reload_tools(monkeypatch, tmp_path):
    monkeypatch.setenv("LOCAL_DOC_AGENT_WORKSPACE", str(tmp_path / "workspace"))
    monkeypatch.setenv("LOCAL_DOC_AGENT_LOGS", str(tmp_path / "logs"))

    import server.config as config
    import server.logging_utils as logging_utils
    import server.tools_files as tools_files

    importlib.reload(config)
    importlib.reload(logging_utils)
    importlib.reload(tools_files)
    return tools_files


def test_rejects_paths_outside_workspace(monkeypatch, tmp_path):
    tools = _reload_tools(monkeypatch, tmp_path)

    result = tools.write_text_file_tool("../escape.md", "bad")
    assert result["ok"] is False
    assert "workspace" in result["error"]


def test_rejects_non_text_extension_for_text_tools(monkeypatch, tmp_path):
    tools = _reload_tools(monkeypatch, tmp_path)

    result = tools.write_text_file_tool("docs/file.exe", "bad")
    assert result["ok"] is False
    assert "확장자" in result["error"]
