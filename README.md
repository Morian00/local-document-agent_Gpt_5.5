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
- 1단계 Markdown 작성 도구
  - `create_markdown`
- 2단계 문서 변환 도구
  - `export_docx_from_markdown`
  - `extract_docx_text`
  - `create_xlsx_from_sheets`
  - `create_pptx_from_spec`
- 3단계 이미지 도구
  - `list_assets`
  - `save_base64_image`
  - `insert_image_to_markdown`
  - `insert_image_to_pptx`
- 4단계 템플릿 도구
  - `list_templates`
  - `create_markdown_from_template`
  - `create_docx_from_template`
  - `create_pptx_from_template`
- workspace 밖 경로 차단
- 기존 파일 자동 백업
- diff summary 반환
- JSONL 작업 로그
- pytest 테스트 코드
- 이미지 도구 모듈 분리

DOCX, PPTX, XLSX, 이미지, 템플릿 기능은 로컬 MCP 클라이언트 기준으로 동작 검증이 완료되었다.

## 현재 작업 상태

- 로컬 구현: 0단계 MVP 완료
- 1단계 구현: Markdown 신규 생성 도구 추가
- 2단계 구현: Markdown 기반 DOCX 변환 도구 추가
- 2단계 구현: 기존 DOCX 텍스트 추출 도구 추가
- 2단계 구현: XLSX 신규 생성 도구 추가
- 2단계 구현: PPTX 신규 생성 도구 추가
- 3단계 구현: assets 이미지 저장, 목록 조회, Markdown 삽입 도구 추가
- 3단계 구현: PPTX 이미지 삽입 도구 추가
- 유지보수 정리: 이미지 도구를 `server/tools_assets.py`로 분리
- 4단계 구현: Markdown, DOCX, PPTX 템플릿 기반 문서 생성 도구 추가
- 품질 고도화: DOCX 기본 스타일 프로필 적용
- 품질 고도화: PPTX 기본 스타일 프로필 적용
- 입력 품질 가드: 인코딩 손상 의심 연속 물음표 차단
- 로컬 테스트: `uv run pytest` 기준 36개 통과
- 로컬 MCP 클라이언트 배치 스모크 검증: 18개 도구 통과
- Git 원격 저장소: `origin/main` 연결 완료
- 다음 확인 대상: ChatGPT UI Thinking 모드 기준 PPTX, 이미지, 템플릿 도구 최종 호출 확인

아직 확정되지 않은 항목:

- 쓰기 도구 반복 호출 시 권한 확인 모달 또는 제한 발생 패턴
- ChatGPT UI에서 `create_pptx_from_spec` 호출 성공 여부
- ChatGPT UI에서 `extract_docx_text` 호출 성공 여부
- ChatGPT UI에서 이미지 도구 호출 성공 여부
- ChatGPT UI에서 템플릿 도구 호출 성공 여부
- GPT Pro 모델 MCP 미노출 제약의 지속 여부
- 슬라이드 품질 고도화 범위

## 문서

- 계획서: [local-document-agent-plan.md](local-document-agent-plan.md)
- 구현 프로젝트: [local-doc-agent/README.md](local-doc-agent/README.md)
- MVP 상태: [local-doc-agent/MVP_STATUS.md](local-doc-agent/MVP_STATUS.md)

## 실행 요약

Python 3.12+와 `uv` 설치 후:

```powershell
cd local-doc-agent
uv sync
Copy-Item .env.example .env
.\scripts\start_server.ps1
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
3. 경로 선택: `C:\Users\home\Desktop\local-document-agent_Gpt_5.5`
4. 변경 파일 확인
5. 커밋 메시지 입력
6. Commit to main 선택
7. Publish repository 선택

현재 원격 저장소:

```text
https://github.com/Morian00/local-document-agent_Gpt_5.5.git
```
