# Local Document Agent MVP 상태

## 판정

개인용 로컬 문서 작업 MCP MVP 1차 구현 완료.

로컬 MCP 서버, ngrok 터널, ChatGPT 커스텀 커넥터 연결, 파일 읽기·쓰기·수정, 문서 생성, 이미지 삽입 루프가 검증된 상태다.

## 완료 기능

- FastMCP 기반 `/mcp` 서버
- workspace 내부 경로 제한
- 텍스트 파일 목록 조회, 읽기, 쓰기, 패치
- 기존 파일 자동 백업
- JSONL 작업 로그
- Markdown 구조화 문서 생성
- Markdown 기반 DOCX 생성
- 시트 목록 기반 XLSX 생성
- 슬라이드 spec 기반 PPTX 생성
- assets 이미지 목록 조회
- base64 이미지 저장
- Markdown 이미지 링크 삽입
- PPTX 이미지 삽입
- 이미지 도구 모듈 분리
- 템플릿 목록 조회
- 템플릿 기반 Markdown 생성

## 노출 도구

- `ping`
- `list_files`
- `list_assets`
- `list_templates`
- `read_text_file`
- `write_text_file`
- `create_markdown`
- `create_markdown_from_template`
- `export_docx_from_markdown`
- `create_xlsx_from_sheets`
- `create_pptx_from_spec`
- `save_base64_image`
- `insert_image_to_markdown`
- `insert_image_to_pptx`
- `patch_text_file`

## 검증 상태

- 로컬 테스트: `uv run pytest` 기준 23개 통과
- 로컬 MCP 클라이언트 기준 전체 도구 노출 확인
- ngrok HTTPS 경유 MCP 호출 확인
- ChatGPT UI 기준 0~1단계 및 DOCX 변환 호출 확인
- 로컬 MCP 클라이언트 기준 템플릿 도구 호출 확인

## 남은 확인

- ChatGPT UI 기준 `create_xlsx_from_sheets` 최종 호출 확인
- ChatGPT UI 기준 `create_pptx_from_spec` 최종 호출 확인
- ChatGPT UI 기준 이미지 도구 4종 최종 호출 확인
- ChatGPT UI 기준 템플릿 도구 2종 최종 호출 확인
- 쓰기 도구 반복 호출 시 권한 확인 모달 발생 패턴 기록

## MVP 이후 후보

- 템플릿 기반 DOCX, PPTX 생성
- PPTX 레이아웃 품질 고도화
- DOCX 스타일 고도화
- XLSX 서식 옵션 확대
- 기존 DOCX 텍스트 추출
- 기존 DOCX to Markdown 변환
- 도구 모듈 추가 분리
