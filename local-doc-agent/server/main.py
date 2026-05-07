from __future__ import annotations

import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from server.config import ensure_base_directories, settings
    from server.tools_files import (
        list_files_tool,
        patch_text_file_tool,
        ping_tool,
        read_text_file_tool,
        write_text_file_tool,
    )
else:
    from .config import ensure_base_directories, settings
    from .tools_files import (
        list_files_tool,
        patch_text_file_tool,
        ping_tool,
        read_text_file_tool,
        write_text_file_tool,
    )


mcp = FastMCP(
    "Local Document Agent",
    host=settings.host,
    port=settings.port,
    streamable_http_path="/mcp",
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
def ping() -> dict:
    """Check whether the local document MCP server is reachable."""
    return ping_tool()


@mcp.tool()
def list_files(
    path: str = ".",
    recursive: bool = True,
    extensions: list[str] | None = None,
) -> dict:
    """List files inside the configured workspace root."""
    return list_files_tool(path=path, recursive=recursive, extensions=extensions)


@mcp.tool()
def read_text_file(path: str, max_chars: int | None = None) -> dict:
    """Read a UTF-8 text file inside the workspace root."""
    return read_text_file_tool(path=path, max_chars=max_chars)


@mcp.tool()
def write_text_file(
    path: str,
    content: str,
    overwrite: bool | None = None,
    create_backup: bool | None = None,
) -> dict:
    """Create or overwrite a UTF-8 text file inside the workspace root."""
    return write_text_file_tool(
        path=path,
        content=content,
        overwrite=overwrite,
        create_backup=create_backup,
    )


@mcp.tool()
def patch_text_file(
    path: str,
    replacements: list[dict],
    create_backup: bool | None = None,
) -> dict:
    """Patch a text file with find/replace operations inside the workspace root."""
    return patch_text_file_tool(
        path=path,
        replacements=replacements,
        create_backup=create_backup,
    )


def main() -> None:
    ensure_base_directories()
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
