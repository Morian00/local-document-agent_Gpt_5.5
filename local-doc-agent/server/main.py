from __future__ import annotations

import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from server.config import ensure_base_directories, settings
    from server.tools_files import (
        create_markdown_tool,
        create_pptx_from_spec_tool,
        create_xlsx_from_sheets_tool,
        extract_docx_text_tool,
        extract_xlsx_text_tool,
        export_docx_from_markdown_tool,
        insert_image_to_markdown_tool,
        insert_image_to_pptx_tool,
        list_assets_tool,
        list_files_tool,
        patch_text_file_tool,
        ping_tool,
        read_text_file_tool,
        save_base64_image_tool,
        write_text_file_tool,
    )
    from server.tools_templates import (
        create_docx_from_template_tool,
        create_markdown_from_template_tool,
        create_pptx_from_template_tool,
        list_templates_tool,
    )
else:
    from .config import ensure_base_directories, settings
    from .tools_files import (
        create_markdown_tool,
        create_pptx_from_spec_tool,
        create_xlsx_from_sheets_tool,
        extract_docx_text_tool,
        extract_xlsx_text_tool,
        export_docx_from_markdown_tool,
        insert_image_to_markdown_tool,
        insert_image_to_pptx_tool,
        list_assets_tool,
        list_files_tool,
        patch_text_file_tool,
        ping_tool,
        read_text_file_tool,
        save_base64_image_tool,
        write_text_file_tool,
    )
    from .tools_templates import (
        create_docx_from_template_tool,
        create_markdown_from_template_tool,
        create_pptx_from_template_tool,
        list_templates_tool,
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
def list_assets(
    path: str = "assets",
    recursive: bool = True,
    extensions: list[str] | None = None,
) -> dict:
    """List image assets inside the configured workspace root."""
    return list_assets_tool(path=path, recursive=recursive, extensions=extensions)


@mcp.tool()
def list_templates() -> dict:
    """List built-in document templates."""
    return list_templates_tool()


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
def create_markdown(
    path: str,
    title: str,
    summary: str | None = None,
    sections: list[dict] | None = None,
    overwrite: bool | None = None,
    create_backup: bool | None = None,
) -> dict:
    """Create a Markdown document from a title, summary, and section list."""
    return create_markdown_tool(
        path=path,
        title=title,
        summary=summary,
        sections=sections,
        overwrite=overwrite,
        create_backup=create_backup,
    )


@mcp.tool()
def create_markdown_from_template(
    template_name: str,
    output_path: str,
    title: str,
    summary: str = "",
    variables: dict | None = None,
    overwrite: bool | None = None,
    create_backup: bool | None = None,
) -> dict:
    """Create a Markdown document from a built-in template."""
    return create_markdown_from_template_tool(
        template_name=template_name,
        output_path=output_path,
        title=title,
        summary=summary,
        variables=variables,
        overwrite=overwrite,
        create_backup=create_backup,
    )


@mcp.tool()
def create_docx_from_template(
    template_name: str,
    output_path: str,
    title: str,
    summary: str = "",
    variables: dict | None = None,
    overwrite: bool | None = None,
    create_backup: bool | None = None,
) -> dict:
    """Create a DOCX document from a built-in template."""
    return create_docx_from_template_tool(
        template_name=template_name,
        output_path=output_path,
        title=title,
        summary=summary,
        variables=variables,
        overwrite=overwrite,
        create_backup=create_backup,
    )


@mcp.tool()
def create_pptx_from_template(
    template_name: str,
    output_path: str,
    title: str,
    summary: str = "",
    variables: dict | None = None,
    overwrite: bool | None = None,
    create_backup: bool | None = None,
) -> dict:
    """Create a PPTX document from a built-in template."""
    return create_pptx_from_template_tool(
        template_name=template_name,
        output_path=output_path,
        title=title,
        summary=summary,
        variables=variables,
        overwrite=overwrite,
        create_backup=create_backup,
    )


@mcp.tool()
def export_docx_from_markdown(
    source_path: str,
    output_path: str,
    overwrite: bool | None = None,
    create_backup: bool | None = None,
) -> dict:
    """Export a Markdown file inside the workspace to a DOCX file."""
    return export_docx_from_markdown_tool(
        source_path=source_path,
        output_path=output_path,
        overwrite=overwrite,
        create_backup=create_backup,
    )


@mcp.tool()
def extract_docx_text(
    source_path: str,
    max_chars: int | None = None,
    include_paragraphs: bool = True,
) -> dict:
    """Extract text from a DOCX file inside the workspace."""
    return extract_docx_text_tool(
        source_path=source_path,
        max_chars=max_chars,
        include_paragraphs=include_paragraphs,
    )


@mcp.tool()
def create_xlsx_from_sheets(
    output_path: str,
    sheets: list[dict],
    overwrite: bool | None = None,
    create_backup: bool | None = None,
) -> dict:
    """Create an XLSX workbook from sheet specs inside the workspace."""
    return create_xlsx_from_sheets_tool(
        output_path=output_path,
        sheets=sheets,
        overwrite=overwrite,
        create_backup=create_backup,
    )


@mcp.tool()
def extract_xlsx_text(
    source_path: str,
    query: str | None = None,
    max_cells: int = 5000,
    max_chars: int | None = None,
) -> dict:
    """Extract and optionally search cell text from an XLSX file inside the workspace."""
    return extract_xlsx_text_tool(
        source_path=source_path,
        query=query,
        max_cells=max_cells,
        max_chars=max_chars,
    )


@mcp.tool()
def create_pptx_from_spec(
    output_path: str,
    title: str,
    slides: list[dict],
    subtitle: str | None = None,
    overwrite: bool | None = None,
    create_backup: bool | None = None,
) -> dict:
    """Create a PPTX deck from a simple slide spec inside the workspace."""
    return create_pptx_from_spec_tool(
        output_path=output_path,
        title=title,
        slides=slides,
        subtitle=subtitle,
        overwrite=overwrite,
        create_backup=create_backup,
    )


@mcp.tool()
def save_base64_image(
    output_path: str,
    image_base64: str,
    overwrite: bool | None = None,
    create_backup: bool | None = None,
) -> dict:
    """Save a base64-encoded image inside the workspace."""
    return save_base64_image_tool(
        output_path=output_path,
        image_base64=image_base64,
        overwrite=overwrite,
        create_backup=create_backup,
    )


@mcp.tool()
def insert_image_to_markdown(
    markdown_path: str,
    image_path: str,
    alt_text: str = "",
    position: str = "append",
    create_backup: bool | None = None,
) -> dict:
    """Insert an image reference into a Markdown file inside the workspace."""
    return insert_image_to_markdown_tool(
        markdown_path=markdown_path,
        image_path=image_path,
        alt_text=alt_text,
        position=position,
        create_backup=create_backup,
    )


@mcp.tool()
def insert_image_to_pptx(
    pptx_path: str,
    image_path: str,
    slide_index: int = 0,
    left: float = 1.0,
    top: float = 1.5,
    width: float | None = 4.0,
    height: float | None = None,
    create_backup: bool | None = None,
) -> dict:
    """Insert an image into a PPTX slide inside the workspace."""
    return insert_image_to_pptx_tool(
        pptx_path=pptx_path,
        image_path=image_path,
        slide_index=slide_index,
        left=left,
        top=top,
        width=width,
        height=height,
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
