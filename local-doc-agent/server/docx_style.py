from __future__ import annotations

from typing import Any


DOCX_STYLE_PROFILE = "default_korean_docx_v1"
DOCX_BODY_FONT = "Malgun Gothic"


def _set_font(style: Any, *, name: str, size_pt: float, bold: bool | None = None) -> None:
    from docx.oxml.ns import qn
    from docx.shared import Pt

    font = style.font
    font.name = name
    font.size = Pt(size_pt)
    if bold is not None:
        font.bold = bold

    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.rFonts
    if rfonts is not None:
        rfonts.set(qn("w:eastAsia"), name)


def apply_docx_style(document: Any) -> str:
    from docx.shared import Inches, Pt

    for section in document.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)

    normal = document.styles["Normal"]
    _set_font(normal, name=DOCX_BODY_FONT, size_pt=10.5)
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(6)

    heading_sizes = {
        "Title": 22,
        "Heading 1": 18,
        "Heading 2": 15,
        "Heading 3": 13,
        "Heading 4": 12,
    }
    for style_name, size in heading_sizes.items():
        if style_name in document.styles:
            style = document.styles[style_name]
            _set_font(style, name=DOCX_BODY_FONT, size_pt=size, bold=True)
            style.paragraph_format.space_before = Pt(8)
            style.paragraph_format.space_after = Pt(6)

    for style_name in ("List Bullet", "List Number"):
        if style_name in document.styles:
            style = document.styles[style_name]
            _set_font(style, name=DOCX_BODY_FONT, size_pt=10.5)
            style.paragraph_format.space_after = Pt(3)

    return DOCX_STYLE_PROFILE
