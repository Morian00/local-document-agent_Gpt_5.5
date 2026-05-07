# ChatGPT 커스텀 커넥터 검증 체크리스트

## 목적

로컬 MCP 서버가 ChatGPT 개발자 모드 커스텀 커넥터에서 실제 호출 가능한지 확인한다.
로컬 테스트 통과와 ChatGPT UI 호출 가능 여부는 별도 검증 대상으로 분리한다.

## 현재 로컬 검증 상태

- 로컬 서버 실행 확인 완료
- 로컬 MCP 엔드포인트: `http://127.0.0.1:2091/mcp`
- MCP 클라이언트 기준 도구 목록 조회 성공
- `ping` 호출 성공
- 로컬 pytest 기준 통과: 29개 테스트
- 배치 스모크 검증 스크립트 기준 주요 도구 17개 일괄 호출 성공

## 현재 ChatGPT UI 검증 상태

- 커스텀 커넥터 등록 완료
- ngrok HTTPS 터널 연결 완료
- ChatGPT UI 기준 `ping` 호출 성공
- ChatGPT UI 기준 `list_files` 호출 성공
- ChatGPT UI 기준 `write_text_file` 호출 성공
- ChatGPT UI 기준 `patch_text_file` 호출 성공
- ChatGPT UI 기준 `create_markdown` 호출 성공
- 기존 파일 수정 시 백업 생성 확인 완료
- 오류 반환 로그 기록 확인 완료
- 0~1단계 MVP 검증 완료
- ChatGPT UI 기준 `export_docx_from_markdown` 호출 성공
- ChatGPT UI 기준 `create_xlsx_from_sheets` 호출 성공
- 로컬 MCP 클라이언트 기준 `create_pptx_from_spec` 호출 성공
- 로컬 MCP 클라이언트 기준 `list_assets`, `save_base64_image`, `insert_image_to_markdown` 호출 성공
- 로컬 MCP 클라이언트 기준 `insert_image_to_pptx` 호출 성공
- 로컬 MCP 클라이언트 기준 `list_templates`, `create_markdown_from_template`, `create_docx_from_template`, `create_pptx_from_template` 호출 성공

## 현재 UI 제약

- GPT Pro 모델에서는 현재 MCP 도구가 노출되지 않을 수 있음
- Thinking 모드에서 커스텀 커넥터 MCP 도구 호출 필요
- 모델·모드별 MCP 노출 정책은 ChatGPT UI 정책 변경 가능성 존재
- 검증 시점, 사용 모델, 사용 모드를 함께 기록 권장

현재 노출 도구:

- `ping`
- `list_files`
- `list_templates`
- `read_text_file`
- `write_text_file`
- `create_markdown`
- `create_markdown_from_template`
- `create_docx_from_template`
- `create_pptx_from_template`
- `export_docx_from_markdown`
- `create_xlsx_from_sheets`
- `create_pptx_from_spec`
- `list_assets`
- `save_base64_image`
- `insert_image_to_markdown`
- `insert_image_to_pptx`
- `patch_text_file`

## 외부 연결 준비

필요 항목:

- 로컬 서버 실행 상태 유지
- HTTPS 터널 도구 설치
- ChatGPT 개발자 모드 커스텀 커넥터 접근 권한

MVP 검증은 ngrok만 사용한다.
Cloudflare Tunnel은 고정 도메인, 운영 안정성, 장기 운영이 필요해졌을 때 검토한다.

ngrok 실행 예시:

```powershell
ngrok http 2091 --host-header localhost:2091
```

`--host-header` 옵션 없이 실행할 경우, 환경에 따라 외부 MCP 클라이언트 호출에서 421 응답이 발생할 수 있다.

터널 실행 후 HTTPS 주소 뒤에 `/mcp`를 붙여 커넥터에 등록한다.

예시:

```text
https://example.ngrok-free.app/mcp
```

## ChatGPT UI 검증 순서

1. 로컬 서버 실행
2. HTTPS 터널 실행
3. 터널 HTTPS 주소 확인
4. ChatGPT 개발자 모드 커스텀 커넥터 생성
5. 커넥터 MCP URL에 `https://.../mcp` 입력
6. 도구 목록 노출 확인: 완료
7. `ping` 호출 확인: 완료
8. `list_files` 호출 확인: 완료
9. `write_text_file`로 테스트 Markdown 파일 생성: 완료
10. `patch_text_file`로 테스트 Markdown 파일 수정: 완료
11. `create_markdown`으로 구조화 Markdown 문서 생성: 완료
12. `export_docx_from_markdown`으로 DOCX 파일 생성: 완료
13. `create_xlsx_from_sheets`로 XLSX 파일 생성
14. `create_pptx_from_spec`로 PPTX 파일 생성
15. `save_base64_image`로 이미지 저장
16. `list_assets`로 이미지 목록 조회
17. `insert_image_to_markdown`으로 Markdown 이미지 링크 삽입
18. `insert_image_to_pptx`로 PPTX 이미지 삽입
19. `list_templates`로 템플릿 목록 조회
20. `create_markdown_from_template`으로 템플릿 기반 Markdown 생성
21. `create_docx_from_template`으로 템플릿 기반 DOCX 생성
22. `create_pptx_from_template`으로 템플릿 기반 PPTX 생성
23. 권한 확인 모달, 호출 제한, 오류 메시지 기록: 진행 중

## 배치 스모크 검증

개별 도구 수동 검증은 초기 연결 확인에만 사용한다.
기능 회귀 확인은 로컬 MCP 클라이언트 배치 스모크 검증을 우선한다.

실행 명령:

```powershell
uv run python scripts/smoke_mcp.py --url http://127.0.0.1:2091/mcp
```

HTTPS 터널 경유 검증:

```powershell
uv run python scripts/smoke_mcp.py --url https://example.ngrok-free.app/mcp
```

배치 검증 범위:

- `ping`
- `list_files`
- `write_text_file`
- `read_text_file`
- `patch_text_file`
- `create_markdown`
- `export_docx_from_markdown`
- `create_xlsx_from_sheets`
- `create_pptx_from_spec`
- `save_base64_image`
- `list_assets`
- `insert_image_to_markdown`
- `insert_image_to_pptx`
- `list_templates`
- `create_markdown_from_template`
- `create_docx_from_template`
- `create_pptx_from_template`

## 성공 기준

- ChatGPT UI에서 도구 목록 확인 가능
- `ping` 호출 성공
- workspace 내부 파일 목록 조회 가능
- workspace 내부 Markdown 파일 생성 가능
- 기존 Markdown 파일 수정 가능
- `create_markdown` 호출로 문서 생성 가능
- `export_docx_from_markdown` 호출로 DOCX 생성 가능
- DOCX 출력에 기본 스타일 프로필 적용 가능
- `create_xlsx_from_sheets` 호출로 XLSX 생성 가능
- `create_pptx_from_spec` 호출로 PPTX 생성 가능
- PPTX 출력에 기본 스타일 프로필 적용 가능
- `save_base64_image` 호출로 이미지 저장 가능
- `list_assets` 호출로 이미지 목록 조회 가능
- `insert_image_to_markdown` 호출로 Markdown 이미지 링크 삽입 가능
- `insert_image_to_pptx` 호출로 PPTX 이미지 삽입 가능
- `list_templates` 호출로 템플릿 목록 조회 가능
- `create_markdown_from_template` 호출로 템플릿 기반 Markdown 생성 가능
- `create_docx_from_template` 호출로 템플릿 기반 DOCX 생성 가능
- 템플릿 기반 DOCX 출력에 기본 스타일 프로필 적용 가능
- `create_pptx_from_template` 호출로 템플릿 기반 PPTX 생성 가능
- 템플릿 기반 PPTX 출력에 기본 스타일 프로필 적용 가능
- 오류 발생 시 오류 메시지가 ChatGPT 응답에 반환됨

현재 완료 항목:

- `ping`
- `list_files`
- `write_text_file`
- `patch_text_file`
- 자동 백업
- 작업 로그
- 오류 반환
- `create_markdown`
- `export_docx_from_markdown`
- `create_xlsx_from_sheets`
- 로컬 MCP 클라이언트 배치 스모크 검증: 17개 도구 통과

다음 확인 항목:

- ChatGPT UI Thinking 모드 기준 남은 도구 최종 확인
- GPT Pro 모델 MCP 미노출 제약 기록 유지
- `create_pptx_from_spec`
- 이미지 도구 4종
- 템플릿 도구 4종

## 커밋 전 상태

- 로컬 테스트 통과: 29개
- 민감값 저장소 포함 여부 확인: 포함 없음
- 런타임 산출물은 `.gitignore`로 제외
- `uv.lock` 생성됨
- 이미지 도구는 `server/tools_assets.py`로 분리됨
- 템플릿 도구는 `server/tools_templates.py`로 분리됨

## 0~1단계 판정

0~1단계 MVP 검증 완료.

완료 근거:

- ChatGPT UI에서 로컬 MCP 도구 호출 가능
- 파일 목록 조회 가능
- Markdown 파일 생성 가능
- Markdown 파일 읽기 가능
- Markdown 파일 수정 가능
- 기존 파일 수정 시 백업 생성 가능
- 구조화 Markdown 문서 생성 가능
- 작업 로그 기록 가능
- 오류 응답 반환 가능

## DOCX 변환 검증 요청 예시

```text
로컬 문서 MCP의 export_docx_from_markdown을 호출해서 docs/structured-test.md를 output/structured-test.docx로 변환해줘.
```

## XLSX 생성 검증 요청 예시

```text
로컬 문서 MCP의 create_xlsx_from_sheets를 호출해서 output/sample-checklist.xlsx 파일을 만들어줘. 시트 이름은 Checklist, 헤더는 항목, 담당, 상태로 하고, 행은 "DOCX 검증/Planner/완료", "XLSX 검증/Planner/진행 중"으로 넣어줘.
```

## PPTX 생성 검증 요청 예시

```text
로컬 문서 MCP의 create_pptx_from_spec을 호출해서 output/sample-deck-chatgpt.pptx 파일을 만들어줘. 제목은 Local Document Agent, 부제는 MVP 변환 테스트로 하고, 슬라이드는 "검증 완료"와 "다음 작업" 2장으로 구성해줘. 첫 슬라이드는 Markdown, DOCX, XLSX, PPTX 불릿을 넣고, 두 번째 슬라이드는 템플릿과 품질 개선을 본문으로 넣어줘.
```

## 이미지 도구 검증 요청 예시

```text
로컬 문서 MCP의 list_assets를 호출해서 assets 이미지 목록을 보여줘. 그 다음 insert_image_to_markdown을 호출해서 docs/structured-test.md 하단에 assets/sample-pixel.png 이미지를 "Sample pixel" alt 텍스트로 삽입해줘.
```

## PPTX 이미지 삽입 검증 요청 예시

```text
로컬 문서 MCP의 insert_image_to_pptx를 호출해서 output/sample-deck.pptx의 두 번째 슬라이드에 assets/sample-pixel.png 이미지를 넣어줘. slide_index는 1, left는 8.0, top은 1.5, width는 1.0으로 설정해줘.
```

## 템플릿 검증 요청 예시

```text
로컬 문서 MCP의 list_templates를 호출해서 사용 가능한 템플릿 목록을 보여줘. 그 다음 create_markdown_from_template을 호출해서 planning_doc 템플릿으로 docs/template-chatgpt.md 파일을 만들어줘. 제목은 전투 시스템 개선안, 요약은 전투 루프와 성장 구조를 정리하는 문서로 해줘.
```

## 템플릿 DOCX 검증 요청 예시

```text
로컬 문서 MCP의 create_docx_from_template을 호출해서 proposal_doc 템플릿으로 output/template-proposal-chatgpt.docx 파일을 만들어줘. 제목은 문서 자동화 제안서, 요약은 로컬 문서 작업 자동화를 제안하는 문서로 해줘.
```

## 템플릿 PPTX 생성 검증 요청 예시

```text
로컬 문서 MCP의 create_pptx_from_template을 호출해서 planning_doc 템플릿으로 output/template-planning-chatgpt.pptx 파일을 만들어줘. 제목은 전투 시스템 개선안, 요약은 전투 루프와 성장 구조를 정리하는 발표자료로 해줘.
```

## 실패 시 기록 항목

- 터널 도구 종류
- 터널 URL
- ChatGPT 커넥터 등록 시각
- 실패한 도구명
- ChatGPT UI 오류 메시지
- 서버 콘솔 오류 메시지
- `logs/operations.jsonl` 마지막 기록

## 임시 대응

쓰기 도구가 제한될 경우, `ping`, `list_files`, `read_text_file` 중심의 읽기 전용 검증 모드로 전환한다.
읽기 전용 검증이 통과하면 쓰기 도구는 ChatGPT 계정, 워크스페이스, 커넥터 정책을 확인한 뒤 재검증한다.
