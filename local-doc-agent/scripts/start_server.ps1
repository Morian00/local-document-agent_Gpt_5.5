$ErrorActionPreference = "Stop"

Set-Location (Resolve-Path "$PSScriptRoot\..")

chcp 65001 | Out-Null

$utf8 = [System.Text.UTF8Encoding]::new()
[Console]::InputEncoding = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

uv run python -m server.main
