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
- `create_xlsx_from_sheets`
- `create_pptx_from_spec`

`export_docx_from_markdown`은 workspace 내부 Markdown 파일을 읽어 DOCX 파일로 저장한다.
출력 파일은 workspace 내부 경로만 허용하며, 기존 DOCX 파일을 덮어쓸 경우 백업을 생성한다.

`create_xlsx_from_sheets`는 시트 목록, 헤더, 행 데이터를 받아 XLSX 파일을 신규 생성한다.
출력 파일은 workspace 내부 경로만 허용하며, 기존 XLSX 파일을 덮어쓸 경우 백업을 생성한다.

`create_pptx_from_spec`는 제목, 부제, 슬라이드 목록을 받아 PPTX 초안을 신규 생성한다.
출력 파일은 workspace 내부 경로만 허용하며, 기존 PPTX 파일을 덮어쓸 경우 백업을 생성한다.

이미지, 템플릿 기능은 DOCX, XLSX, PPTX 생성이 ChatGPT 개발자 모드에서 실제 동작하는 것을 확인한 뒤 추가한다.

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

## 실행 준비

Python 3.12+와 `uv` 설치가 필요하다.

```powershell
cd local-doc-agent
uv sync
Copy-Item .env.example .env
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
19 passed
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
- 시트 목록 기반 XLSX 생성
- 슬라이드 spec 기반 PPTX 생성
- base64 이미지 저장
- assets 이미지 목록 조회
- Markdown 이미지 링크 삽입
- PPTX 이미지 삽입

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

1. 서버 실행
2. HTTPS 터널 실행
3. ChatGPT 개발자 모드 커스텀 커넥터에 `/mcp` 주소 등록
4. `ping`, `list_files`, `read_text_file` 노출 확인
5. `write_text_file`, `patch_text_file` 실제 호출 가능 여부 확인
6. `create_markdown` 실제 호출 가능 여부 확인
7. `export_docx_from_markdown` 실제 호출 가능 여부 확인
8. `create_xlsx_from_sheets` 실제 호출 가능 여부 확인
9. `create_pptx_from_spec` 실제 호출 가능 여부 확인
10. `list_assets`, `save_base64_image`, `insert_image_to_markdown` 실제 호출 가능 여부 확인
11. `insert_image_to_pptx` 실제 호출 가능 여부 확인
12. 권한 확인 모달 또는 호출 제한 발생 여부 기록

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
