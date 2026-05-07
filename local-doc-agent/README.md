# Local Document Agent

개인용 로컬 문서 작업 MCP 서버다.
ChatGPT 개발자 모드 커스텀 커넥터가 HTTPS 터널의 `/mcp` 엔드포인트를 통해 이 서버의 도구를 호출하고, 서버는 지정된 `workspace` 내부에서만 파일을 읽고 쓴다.

## 0단계 노출 도구

- `ping`
- `list_files`
- `read_text_file`
- `write_text_file`
- `patch_text_file`

## 1단계 Markdown 도구

- `create_markdown`

`create_markdown`은 제목, 요약, 섹션 목록을 받아 Markdown 문서를 생성한다.
저장, 덮어쓰기, 백업, diff summary 반환은 기존 텍스트 파일 도구와 동일한 규칙을 따른다.

## 2단계 문서 변환 도구

- `export_docx_from_markdown`
- `extract_docx_text`
- `create_xlsx_from_sheets`
- `create_pptx_from_spec`

`export_docx_from_markdown`은 workspace 내부 Markdown 파일을 읽어 DOCX 파일로 저장한다.
출력 파일은 workspace 내부 경로만 허용하며, 기존 DOCX 파일을 덮어쓸 경우 백업을 생성한다.
DOCX 출력에는 기본 한글 문서 스타일 프로필을 적용한다.
`extract_docx_text`는 workspace 내부 DOCX 파일에서 문단과 표 텍스트를 추출한다.

`create_xlsx_from_sheets`는 시트 목록, 헤더, 행 데이터를 받아 XLSX 파일을 신규 생성한다.
출력 파일은 workspace 내부 경로만 허용하며, 기존 XLSX 파일을 덮어쓸 경우 백업을 생성한다.

`create_pptx_from_spec`는 제목, 부제, 슬라이드 목록을 받아 PPTX 초안을 신규 생성한다.
출력 파일은 workspace 내부 경로만 허용하며, 기존 PPTX 파일을 덮어쓸 경우 백업을 생성한다.
PPTX 출력에는 기본 한글 발표자료 스타일 프로필을 적용한다.

DOCX, XLSX, PPTX 생성은 로컬 MCP 클라이언트와 ChatGPT UI 기준으로 기본 호출 검증이 완료되었다.

문서·표·발표자료 생성 입력에 인코딩 손상으로 보이는 연속 물음표가 포함될 경우 생성을 거절한다.
깨진 한글이 대량 문서에 누적되는 것을 막기 위한 품질 가드다.

## 3단계 이미지 도구

- `list_assets`
- `save_base64_image`
- `insert_image_to_markdown`
- `insert_image_to_pptx`

`list_assets`는 workspace assets 폴더의 이미지 파일을 조회한다.
`save_base64_image`는 base64 이미지 데이터를 workspace 내부 이미지 파일로 저장한다.
`insert_image_to_markdown`은 Markdown 파일에 이미지 링크를 append 또는 prepend 방식으로 삽입한다.
`insert_image_to_pptx`는 기존 PPTX의 지정 슬라이드에 이미지를 삽입한다.

템플릿 기능은 이미지 저장, Markdown 삽입, PPTX 삽입 흐름이 ChatGPT 개발자 모드에서 실제 동작하는 것을 확인한 뒤 추가한다.

이미지 도구 구현은 `server/tools_assets.py`로 분리되어 있다.
기존 MCP 노출 이름은 유지한다.

## 4단계 템플릿 도구

- `list_templates`
- `create_markdown_from_template`
- `create_docx_from_template`
- `create_pptx_from_template`

`list_templates`는 내장 템플릿 목록을 조회한다.
`create_markdown_from_template`은 템플릿 이름, 제목, 요약, 변수 값을 받아 Markdown 문서 초안을 생성한다.
`create_docx_from_template`은 내장 템플릿을 기반으로 DOCX 문서 초안을 생성한다.
`create_pptx_from_template`은 내장 템플릿을 기반으로 PPTX 발표자료 초안을 생성한다.

현재 내장 템플릿:

- `planning_doc`
- `proposal_doc`
- `checklist_doc`

## 실행 준비

Python 3.12+와 `uv` 설치가 필요하다.

```powershell
cd local-doc-agent
uv sync
Copy-Item .env.example .env
.\scripts\start_server.ps1
```

Windows PowerShell에서 직접 실행할 경우 서버 시작 전에 UTF-8 환경을 먼저 고정한다.

```powershell
chcp 65001
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new()
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$OutputEncoding = [System.Text.UTF8Encoding]::new()
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
uv run python -m server.main
```

기본 MCP 엔드포인트:

```text
http://127.0.0.1:2091/mcp
```

## MCP Inspector 확인

```powershell
uv run mcp dev server/main.py
```

또는 서버 실행 후 MCP Inspector에서 다음 주소로 연결한다.

```text
http://127.0.0.1:2091/mcp
```

## 로컬 테스트

```powershell
uv run pytest
```

현재 확인 결과:

```text
36 passed
```

테스트 범위:

- workspace 밖 경로 차단
- 텍스트 확장자 제한
- 파일 생성
- 파일 읽기
- find/replace 패치
- 기존 파일 자동 백업
- 확장자 필터 기반 파일 목록 조회
- Markdown 기반 DOCX 생성
- DOCX 기본 스타일 프로필 적용
- 기존 DOCX 텍스트 추출
- 인코딩 손상 의심 연속 물음표 입력 차단
- 시트 목록 기반 XLSX 생성
- 슬라이드 spec 기반 PPTX 생성
- PPTX 기본 스타일 프로필 적용
- base64 이미지 저장
- assets 이미지 목록 조회
- Markdown 이미지 링크 삽입
- PPTX 이미지 삽입
- 템플릿 목록 조회
- 템플릿 기반 Markdown 생성
- 템플릿 기반 DOCX 생성
- 템플릿 기반 PPTX 생성

## 배치 스모크 검증

MCP 연결 검증은 개별 도구를 하나씩 확인하는 방식보다 배치 스모크 검증을 우선한다.
서버 실행 후 다음 명령으로 주요 도구를 한 번에 호출한다.

```powershell
uv run python scripts/smoke_mcp.py --url http://127.0.0.1:2091/mcp
```

ngrok 경유 확인이 필요할 경우 URL만 교체한다.

```powershell
uv run python scripts/smoke_mcp.py --url https://example.ngrok-free.app/mcp
```

검증 대상:

- 연결 확인
- 파일 목록, 읽기, 쓰기, 패치
- Markdown 생성
- DOCX 생성 및 텍스트 추출, XLSX, PPTX 생성
- 이미지 저장 및 삽입
- 템플릿 목록, Markdown 템플릿, DOCX 템플릿, PPTX 템플릿 생성

## HTTPS 터널

ngrok 예시:

```powershell
ngrok http 2091
```

ChatGPT 개발자 모드 커스텀 커넥터에는 ngrok이 발급한 HTTPS 주소 뒤에 `/mcp`를 붙여 등록한다.

```text
https://example.ngrok-free.app/mcp
```

## 다음 작업

1. 배치 스모크 검증 스크립트 유지
2. ChatGPT UI 모드별 MCP 도구 노출 제약 기록
3. 기존 DOCX to Markdown 변환 검토
4. XLSX 서식 옵션 확대 검토
5. ChatGPT UI Thinking 모드 기준 신규 도구 호출 확인

쓰기 도구가 제한될 경우, 1차 대응은 읽기 전용 검증 모드로 전환한다.

상세 검증 절차는 [CONNECTOR_CHECKLIST.md](CONNECTOR_CHECKLIST.md)를 기준으로 진행한다.

## 작업 폴더

기본 구조:

```text
workspace/
  docs/
  assets/
  output/
  backups/
logs/
  operations.jsonl
```

서버는 `workspace` 밖으로 나가는 경로를 거부한다.
기존 파일을 덮어쓸 때는 `workspace/backups` 아래에 자동 백업을 생성하고, 결과에 `diff_summary`를 반환한다.
