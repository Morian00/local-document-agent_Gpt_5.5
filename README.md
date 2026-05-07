# Local Document Agent

웹 ChatGPT 개발자 모드 커스텀 커넥터에서 호출할 수 있는 개인용 로컬 문서 작업 MCP 서버 프로젝트다.

목표는 웹 ChatGPT가 문서 내용을 작성하고, 로컬 Python MCP 서버가 지정된 `workspace` 폴더 안에서 파일 읽기, 쓰기, 수정, 백업, 로그 기록을 실행하는 구조를 검증하는 것이다.

## 현재 구현 범위

- FastMCP 기반 `/mcp` 서버 골격
- 초기 커넥터 노출 도구 5개
  - `ping`
  - `list_files`
  - `read_text_file`
  - `write_text_file`
  - `patch_text_file`
- workspace 밖 경로 차단
- 기존 파일 자동 백업
- diff summary 반환
- JSONL 작업 로그
- pytest 테스트 코드

DOCX, PPTX, XLSX, 이미지, 템플릿 기능은 파일 읽기/쓰기 루프가 ChatGPT 개발자 모드에서 실제로 동작하는 것을 확인한 뒤 추가한다.

## 문서

- 계획서: [local-document-agent-plan.md](local-document-agent-plan.md)
- 구현 프로젝트: [local-doc-agent/README.md](local-doc-agent/README.md)

## 실행 요약

Python 3.12+와 `uv` 설치 후:

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

## GitHub Desktop으로 올리기

현재 폴더는 Git 저장소로 초기화되어 있다.
GitHub Desktop에서 아래 순서로 올린다.

1. GitHub Desktop 실행
2. File > Add local repository 선택
3. 경로 선택: `C:\Users\user\Desktop\Gpt_5.5`
4. 변경 파일 확인
5. 커밋 메시지 입력: `Initial local document agent MVP`
6. Commit to main 선택
7. Publish repository 선택

권장 저장소 이름:

```text
local-document-agent
```
