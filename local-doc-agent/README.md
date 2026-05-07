# Local Document Agent

개인용 로컬 문서 작업 MCP 서버다.
ChatGPT 개발자 모드 커스텀 커넥터가 HTTPS 터널의 `/mcp` 엔드포인트를 통해 이 서버의 도구를 호출하고, 서버는 지정된 `workspace` 내부에서만 파일을 읽고 쓴다.

## 0단계 노출 도구

- `ping`
- `list_files`
- `read_text_file`
- `write_text_file`
- `patch_text_file`

DOCX, PPTX, XLSX, 이미지, 템플릿 기능은 파일 읽기/쓰기 루프가 ChatGPT 개발자 모드에서 실제 동작하는 것을 확인한 뒤 추가한다.

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

테스트 범위:

- workspace 밖 경로 차단
- 텍스트 확장자 제한
- 파일 생성
- 파일 읽기
- find/replace 패치
- 기존 파일 자동 백업
- 확장자 필터 기반 파일 목록 조회

## HTTPS 터널

ngrok 예시:

```powershell
ngrok http 2091
```

ChatGPT 개발자 모드 커스텀 커넥터에는 ngrok이 발급한 HTTPS 주소 뒤에 `/mcp`를 붙여 등록한다.

```text
https://example.ngrok-free.app/mcp
```

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
