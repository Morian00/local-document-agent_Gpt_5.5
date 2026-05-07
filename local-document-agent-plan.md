# 웹 ChatGPT용 개인 로컬 문서 작업 MCP 서버 개발 계획서

## 1. 개요

본 문서는 ChatGPT 웹의 개발자 모드와 커스텀 커넥터를 활용하여, 웹 ChatGPT가 사용자의 로컬 작업 폴더에 문서 파일을 생성·수정·변환하는 것처럼 동작하는 도구의 개발 방향을 정리한다.

본 도구의 핵심 목적은 VS Code Codex의 로컬 작업 경험을 코드가 아닌 문서 제작 영역으로 확장하는 것이다.
주요 대상은 기획서, 제안서, 보고서, 포트폴리오, Markdown 문서, DOCX, PPTX, XLSX, 이미지 자료다.

MVP에서는 별도 원격 서버나 별도 실행 계층을 두지 않고, 사용자 PC에서 실행되는 Python 기반 로컬 MCP 문서 서버를 HTTPS 터널로 ChatGPT에 노출한다.

본 계획의 핵심 전제는 다음과 같다.

- 작업 판단 주체: 웹 ChatGPT
- 문서 작성 주체: 웹 ChatGPT
- 도구 호출 주체: 웹 ChatGPT
- 파일 작업 실행 주체: 로컬 MCP 문서 서버
- 로컬 MCP 문서 서버 역할: 파일 I/O, 문서 변환, 이미지 저장, PPTX·XLSX·DOCX 생성

즉, 로컬 MCP 문서 서버는 별도 AI 에이전트가 아니다.
로컬 MCP 문서 서버는 웹 ChatGPT가 호출하는 파일 작업 도구이며, 판단과 작성은 웹 ChatGPT가 담당한다.

## 2. 배경

ChatGPT 개발자 모드는 커스텀 MCP 기반 도구를 ChatGPT 웹에서 사용할 수 있게 하는 기능이다.
읽기 도구를 우선 검증하고, 쓰기·수정 도구는 사용 중인 계정, 워크스페이스, 앱 설정에서 실제 호출 가능한지 0단계에서 확인한다.
본 프로젝트는 쓰기 도구 사용을 목표로 하지만, 초기 연결 검증 단계에서는 write_text_file과 patch_text_file이 실제 ChatGPT UI에서 실행되는지 확인하는 것을 필수 완료 기준으로 둔다.

다만 ChatGPT가 사용자의 로컬 파일 시스템을 직접 탐색하거나, 로컬 경로를 아무 중간 장치 없이 접근하는 구조로 이해해서는 안 된다.
사용자는 로컬 MCP 문서 서버를 실행하고, 이를 HTTPS 터널로 공개한 뒤 ChatGPT 개발자 모드 커넥터에 등록한다.

MVP의 1차 연결 구조는 다음과 같다.

```text
웹 ChatGPT
  → 개발자 모드 커스텀 커넥터
  → HTTPS 터널 주소의 /mcp
  → 로컬 Python MCP 문서 서버
  → workspace 폴더 파일 생성·수정·변환
```

사용자 경험은 다음처럼 설계한다.

```text
사용자 요청
  → 웹 ChatGPT가 문서 작성 및 도구 호출
  → 로컬 MCP 문서 서버가 workspace 내부 파일 작업 수행
  → 결과 경로와 변경 요약을 웹 ChatGPT가 안내
```

별도 원격 릴레이 서버는 MVP 필수 요소가 아니다.
항상 같은 고정 URL, 여러 PC 연결, 장기 세션 관리가 필요해졌을 때 v2 확장안으로 검토한다.

## 3. 제품 정의

본 도구는 개인용 로컬 문서 작업 MCP 서버다.
웹 ChatGPT가 문서 내용을 작성하고, 로컬 MCP 문서 서버가 지정된 workspace 안에서 파일 생성·수정·변환을 실행한다.

제품 성격:

- 웹 ChatGPT 중심 워크플로우
- 개인용 로컬 MCP 문서 서버
- 지정 workspace 기반 파일 작업 도구
- 문서 생성 및 편집 도구
- DOCX·PPTX·XLSX 자동 제작 도구
- 이미지 저장 및 문서 삽입 보조 도구
- 기획서·제안서 제작 특화 도구

제품에서 제외하는 성격:

- 독립형 AI 에이전트
- 로컬 LLM 기반 문서 작성기
- 범용 원격 데스크톱
- 운영체제 전체 제어 도구
- 코드 개발 전용 IDE 대체 도구
- 초기에 별도 원격 릴레이 서버를 운영하는 구조
- 다중 사용자 서비스
- OAuth 기반 권한 관리 시스템
- 항상 켜져 있는 백그라운드 클라우드 서비스

## 4. 목표

### 4.1 사용자 목표

- 웹 ChatGPT만 사용해 로컬 문서 파일 생성
- 웹 ChatGPT만 사용해 기존 문서 수정
- GPT가 생성한 이미지를 로컬 문서에 삽입
- 기획서를 DOCX 제출 문서로 변환
- 기획서를 PPTX 제안서 또는 발표 자료로 변환
- 표, 일정표, 밸런스 데이터, 예산표를 Excel로 생성
- 문서 작성, 정리, 변환, 버전 생성을 하나의 대화 흐름에서 처리

### 4.2 시스템 목표

- ChatGPT 개발자 모드 커스텀 커넥터에서 호출 가능한 MCP 도구 제공
- 로컬 Python MCP 문서 서버 실행
- Streamable HTTP 기반 /mcp 엔드포인트 제공
- ngrok 또는 Cloudflare Tunnel을 통한 HTTPS 터널 연결
- Markdown, TXT, DOCX, PPTX, XLSX, 이미지 파일 작업 지원
- workspace 내부 파일 생성·수정·변환 처리
- 작업 결과를 ChatGPT가 이해하기 쉬운 형태로 반환
- 반복 문서 작업을 도구화

## 5. 핵심 사용 시나리오

### 5.1 Markdown 기획서 작성

사용자가 웹 ChatGPT에 기획서 작성을 요청한다.
ChatGPT는 문서 구조와 본문을 작성한 뒤, MCP 도구를 호출하여 로컬 workspace 폴더에 Markdown 파일을 생성한다.

예시:

- 게임 시스템 기획서 초안 생성
- 제안서 목차 및 본문 작성
- 기존 기획서 리라이팅
- 중복 섹션 정리
- 문서 톤 통일
- 문서 내 표 추가

### 5.2 DOCX 제출 문서 변환

사용자가 Markdown 기획서를 제출용 DOCX로 변환하도록 요청한다.
로컬 MCP 문서 서버는 Pandoc과 reference DOCX 템플릿을 활용하여 Word 문서를 생성한다.

추가로, 기존 DOCX 문서를 읽어 텍스트를 추출하거나 Markdown 초안으로 변환하는 기능을 2단계 이후 선택 기능으로 둔다.
MVP에서는 원본 DOCX의 서식을 정교하게 유지한 채 편집하는 것을 목표로 하지 않는다.
우선 문단과 표 텍스트를 추출하고, ChatGPT가 다시 Markdown 문서로 정리할 수 있게 하는 흐름을 목표로 한다.

예시:

- Markdown 기획서 DOCX 변환
- 회사 제출용 제안서 생성
- 포트폴리오 문서 생성
- reference.docx 기반 스타일 적용
- 기존 DOCX 텍스트 추출
- 기존 DOCX 기반 Markdown 초안 생성

### 5.3 PPTX 제안서 제작

사용자가 웹 ChatGPT에 발표 자료 제작을 요청한다.
ChatGPT는 슬라이드 구성, 제목, 본문, 표, 이미지 배치 지시를 생성하고, MCP 도구를 호출해 PPTX 파일을 만든다.

MVP에서는 Marp 기반 PPTX 생성을 우선한다.
정교한 PPTX 직접 조립은 단순 spec 기반 생성으로 제한한다.

예시:

- Markdown 기획서 기반 PPT 변환
- 제안서 슬라이드 초안 생성
- 프로젝트 소개 자료 제작
- 표지, 문제 정의, 솔루션, 일정, 예산 슬라이드 구성
- GPT 생성 이미지 삽입

### 5.4 XLSX 문서 제작

사용자가 일정표, 데이터 표, 비용표를 요청한다.
ChatGPT는 표 구조와 데이터를 생성하고, MCP 도구를 호출해 XLSX 파일로 저장한다.

예시:

- 개발 일정표
- 콘텐츠 리스트
- 밸런스 데이터 표
- 예산 산정표
- QA 체크리스트
- 제안서 부록용 표

### 5.5 이미지 저장 및 삽입

이미지 기능은 MVP에서 선택적으로 지원한다.
우선 base64 이미지 데이터를 저장하는 도구를 제공하되, ChatGPT 생성 이미지가 항상 MCP 도구 입력으로 직접 전달된다고 가정하지 않는다.
따라서 사용자가 이미지를 workspace/assets에 직접 넣은 뒤 해당 경로를 참조하거나, base64 문자열을 직접 제공하는 흐름도 함께 지원한다.

이후 Markdown 또는 PPTX 생성 단계에서 assets 내부 이미지 경로를 참조하여 삽입한다.

예시:

- assets 폴더 내 콘셉트 이미지 참조
- base64 이미지 데이터 저장
- 제안서 표지 이미지 삽입
- 슬라이드 내 이미지 자동 배치
- Markdown 이미지 링크 추가
- 이미지 파일명 규칙 적용

## 6. 핵심 구조

### 6.1 전체 구조

| 구성 요소 | 역할 |
| --- | --- |
| 웹 ChatGPT | 사용자 대화, 문서 작성, 편집 판단, 도구 호출 |
| 개발자 모드 커스텀 커넥터 | ChatGPT에 로컬 MCP 문서 서버의 도구 목록과 스키마 노출 |
| HTTPS 터널 | 로컬 MCP 서버를 ChatGPT가 접근 가능한 HTTPS 주소로 임시 공개 |
| 로컬 MCP 문서 서버 | 사용자 PC에서 실행되며 파일 생성·수정·변환 수행 |
| workspace 폴더 | 실제 문서, 이미지, 결과물이 저장되는 로컬 작업 공간 |
| 문서 엔진 | Markdown, DOCX, PPTX, XLSX 생성 처리 |
| 작업 로그 | 생성·수정 파일, 요청 요약, 오류 기록 |

### 6.2 책임 분리

| 책임 | 담당 |
| --- | --- |
| 문서 내용 작성 | 웹 ChatGPT |
| 문서 구조 판단 | 웹 ChatGPT |
| 파일명 제안 | 웹 ChatGPT |
| 도구 선택 | 웹 ChatGPT |
| 파일 읽기·쓰기 | 로컬 MCP 문서 서버 |
| Markdown 저장 | 로컬 MCP 문서 서버 |
| DOCX 변환 | 로컬 MCP 문서 서버 |
| PPTX 생성 | 로컬 MCP 문서 서버 |
| XLSX 생성 | 로컬 MCP 문서 서버 |
| 이미지 저장 | 로컬 MCP 문서 서버 |
| 결과 요약 | 웹 ChatGPT |

### 6.3 중요 설계 원칙

- 로컬 MCP 문서 서버에는 별도 LLM을 붙이지 않음
- 로컬 MCP 문서 서버는 판단하지 않고 요청된 작업을 실행
- 문서 품질은 웹 ChatGPT의 지시와 템플릿으로 관리
- 로컬 MCP 문서 서버는 workspace 내부 파일 시스템과 문서 라이브러리 접근만 담당
- ChatGPT가 작업 결과를 다시 읽고 후속 수정을 이어갈 수 있어야 함
- MVP에서는 단순한 연결, 단순한 도구, 빠른 검증을 우선함

## 7. MCP 도구 설계

MVP에서는 승인 대기 후 커밋하는 무거운 구조를 사용하지 않는다.
개인용 도구이므로 바로 쓰기 가능하게 설계하되, 기존 파일을 덮어쓸 때는 자동 백업과 diff 요약을 반환한다.

초기 커넥터 등록 시 모든 도구를 한 번에 노출하지 않는다.
0~1단계에서는 연결 검증과 Markdown 작업에 필요한 최소 도구만 등록한다.
문서 변환 도구와 이미지 도구는 기본 파일 작업 루프가 안정화된 뒤 순차적으로 추가한다.

초기 등록 도구:

- ping
- list_files
- read_text_file
- write_text_file
- patch_text_file

2단계 이후 추가 도구:

- create_markdown
- export_docx_from_markdown
- create_marp_deck
- export_pptx_from_marp
- create_pptx_from_spec
- create_xlsx_from_sheets
- extract_docx_text
- convert_docx_to_markdown

3단계 이후 추가 도구:

- list_assets
- save_base64_image
- insert_image_to_markdown

### 7.1 연결 확인 도구

#### ping

ChatGPT와 로컬 MCP 문서 서버 연결 상태를 확인한다.

입력 예시:

```json
{}
```

출력 예시:

```json
{
  "ok": true,
  "server": "local-doc-agent",
  "workspace": "D:/LocalDocAgent/workspace"
}
```

### 7.2 파일 탐색 도구

#### list_files

작업 폴더 내부 파일 목록을 조회한다.

입력 예시:

```json
{
  "path": ".",
  "recursive": true,
  "extensions": [".md", ".txt", ".docx", ".pptx", ".xlsx", ".png", ".jpg"]
}
```

출력 예시:

```json
{
  "ok": true,
  "root": "D:/LocalDocAgent/workspace",
  "files": [
    "docs/proposal.md",
    "output/proposal.pptx"
  ]
}
```

#### read_text_file

텍스트 기반 문서를 읽는다.

입력 예시:

```json
{
  "path": "docs/proposal.md",
  "max_chars": 50000
}
```

출력 예시:

```json
{
  "ok": true,
  "path": "docs/proposal.md",
  "content": "# 제안서\n\n...",
  "truncated": false
}
```

### 7.3 파일 작성 도구

#### write_text_file

새 텍스트 파일을 생성하거나 기존 텍스트 파일을 덮어쓴다.
기존 파일이 있으면 자동 백업을 만든다.

입력 예시:

```json
{
  "path": "docs/proposal.md",
  "content": "# 제안서\n\n...",
  "overwrite": true,
  "create_backup": true
}
```

출력 예시:

```json
{
  "ok": true,
  "path": "docs/proposal.md",
  "created": false,
  "backup_path": "backups/docs/proposal.20260507-153000.md",
  "diff_summary": {
    "added_lines": 24,
    "removed_lines": 8
  }
}
```

#### patch_text_file

기존 텍스트 파일 일부를 교체한다.
MVP에서는 find/replace 기반으로 시작하되, must_match_once를 지원한다.

입력 예시:

```json
{
  "path": "docs/proposal.md",
  "replacements": [
    {
      "find": "## 3. 기존 섹션",
      "replace": "## 3. 수정된 섹션",
      "must_match_once": true
    }
  ],
  "create_backup": true
}
```

출력 예시:

```json
{
  "ok": true,
  "path": "docs/proposal.md",
  "backup_path": "backups/docs/proposal.20260507-153500.md",
  "changed_count": 1,
  "diff_summary": {
    "added_lines": 3,
    "removed_lines": 2
  }
}
```

### 7.4 문서 생성 도구

#### create_markdown

Markdown 문서를 생성한다.
내부적으로 write_text_file을 재사용해도 된다.

입력 예시:

```json
{
  "path": "docs/game_proposal.md",
  "title": "게임 제안서",
  "content": "# 게임 제안서\n\n...",
  "frontmatter": {
    "project": "Sample Game",
    "version": "v1"
  }
}
```

#### export_docx_from_markdown

Markdown 파일을 DOCX로 변환한다.
MVP에서는 Pandoc 사용을 우선한다.

입력 예시:

```json
{
  "source_md": "docs/game_proposal.md",
  "output_docx": "output/game_proposal.docx",
  "reference_docx": "templates/reference.docx"
}
```

#### extract_docx_text

기존 DOCX 파일에서 텍스트를 추출한다.
MVP에서는 문단과 표 텍스트 추출을 우선하고, 원본 서식 보존 편집은 제외한다.

입력 예시:

```json
{
  "source_docx": "docs/original_proposal.docx",
  "max_chars": 50000
}
```

출력 예시:

```json
{
  "ok": true,
  "source_docx": "docs/original_proposal.docx",
  "content": "문서에서 추출된 텍스트...",
  "truncated": false
}
```

#### convert_docx_to_markdown

기존 DOCX 파일을 Markdown 초안으로 변환한다.
Pandoc 사용을 우선한다.

입력 예시:

```json
{
  "source_docx": "docs/original_proposal.docx",
  "output_md": "docs/original_proposal.converted.md"
}
```

출력 예시:

```json
{
  "ok": true,
  "source_docx": "docs/original_proposal.docx",
  "output_md": "docs/original_proposal.converted.md"
}
```

#### create_marp_deck

Markdown 기반 발표자료를 생성한다.
MVP에서는 PPTX를 바로 정교하게 조립하기보다 Marp용 Markdown을 먼저 만든다.

입력 예시:

```json
{
  "path": "slides/game_proposal.marp.md",
  "title": "게임 제안서",
  "slides": [
    {
      "title": "프로젝트 개요",
      "bullets": ["핵심 콘셉트", "대상 유저", "차별점"]
    }
  ]
}
```

#### export_pptx_from_marp

Marp Markdown 파일을 PPTX로 변환한다.

입력 예시:

```json
{
  "source_marp_md": "slides/game_proposal.marp.md",
  "output_pptx": "output/game_proposal.pptx",
  "theme_css": "templates/marp_theme.css"
}
```

#### create_pptx_from_spec

간단한 슬라이드 명세를 기반으로 PPTX를 직접 생성한다.
MVP에서는 title, bullets, table, image 정도의 단순 레이아웃만 지원한다.

입력 예시:

```json
{
  "path": "output/proposal.pptx",
  "title": "프로젝트 제안서",
  "slides": [
    {
      "layout": "title",
      "title": "프로젝트 제안서",
      "subtitle": "2026"
    },
    {
      "layout": "bullets",
      "title": "핵심 제안",
      "bullets": ["문제 정의", "해결 방향", "기대 효과"]
    }
  ]
}
```

#### create_xlsx_from_sheets

시트 명세를 기반으로 XLSX 파일을 생성한다.

입력 예시:

```json
{
  "path": "output/schedule.xlsx",
  "sheets": [
    {
      "name": "개발 일정",
      "rows": [
        ["단계", "기간", "산출물"],
        ["기획", "2주", "기획서"],
        ["프로토타입", "4주", "플레이 가능 빌드"]
      ],
      "freeze_header": true,
      "auto_filter": true
    }
  ]
}
```

### 7.5 이미지 도구

#### list_assets

assets 폴더 내부 이미지 파일 목록을 조회한다.

입력 예시:

```json
{
  "path": "assets",
  "extensions": [".png", ".jpg", ".jpeg", ".webp"]
}
```

출력 예시:

```json
{
  "ok": true,
  "files": [
    "assets/concept_01.png",
    "assets/title_image.jpg"
  ]
}
```

#### save_base64_image

base64 이미지 데이터를 로컬 파일로 저장한다.
단, ChatGPT 생성 이미지가 MCP 도구 입력으로 직접 전달되지 않는 경우가 있을 수 있으므로, 이 도구는 이미지 저장 보조 기능으로 둔다.
MVP에서는 assets 폴더에 이미 존재하는 이미지 경로를 Markdown, Marp, PPTX 생성 명세에서 참조하는 흐름을 함께 지원한다.

입력 예시:

```json
{
  "path": "assets/concept_01.png",
  "base64_data": "...",
  "overwrite": true
}
```

#### insert_image_to_markdown

Markdown 문서에 이미지 링크를 삽입한다.

입력 예시:

```json
{
  "markdown_path": "docs/proposal.md",
  "image_path": "assets/concept_01.png",
  "alt": "콘셉트 이미지",
  "position": "after_heading",
  "heading": "## 콘셉트"
}
```

#### insert_image_to_pptx

기존 PPTX 수정은 MVP에서 복잡도가 높으므로 선택 기능으로 둔다.
초기에는 create_pptx_from_spec 또는 create_marp_deck 단계에서 이미지를 함께 넣는 방식을 우선한다.

## 8. 기술 구현 방향

### 8.1 권장 구현 조합

| 영역 | 권장 기술 | 비고 |
| --- | --- | --- |
| 언어 | Python 3.12+ | 문서 변환, 파일 처리 라이브러리 활용이 편함 |
| MCP 서버 | Python MCP SDK / FastMCP | 로컬 문서 도구를 MCP tool로 노출 |
| MCP 전송 | Streamable HTTP, 보조로 SSE | ChatGPT 커넥터 연결용 /mcp 엔드포인트 |
| 외부 노출 | ngrok 또는 Cloudflare Tunnel | 개인용 MVP에서는 별도 원격 서버 없이 터널 사용 |
| 패키지 관리 | uv | Python 프로젝트 세팅 단순화 |
| 입력 검증 | Pydantic | 도구 입력 스키마 검증 |
| 파일 처리 | pathlib, shutil, difflib | 경로 처리, 백업, diff 요약 |
| 설정 관리 | .env 또는 config.toml | workspace root, 출력 폴더, 포트 설정 |
| Markdown | 기본 텍스트 처리 + YAML frontmatter 선택 | 기획서 원본 포맷 |
| DOCX 변환 | Pandoc + reference.docx, 보조로 python-docx | 제출용 Word 생성 |
| PPTX 초안 | Marp CLI | Markdown 기반 발표자료 생성 |
| PPTX 직접 생성 | python-pptx | 단순 슬라이드 명세 기반 생성 |
| XLSX 신규 생성 | XlsxWriter | 새 Excel 파일, 서식, 필터, 표 생성에 유리 |
| XLSX 읽기/수정 | openpyxl | 기존 xlsx 읽기·수정 시 사용 |
| 이미지 처리 | Pillow | 리사이즈, 포맷 변환 |
| 작업 로그 | JSONL | 호출 시간, 도구명, 파일 경로, 결과 기록 |
| 테스트 | pytest, MCP Inspector | 도구 단위 테스트 및 MCP 연결 확인 |

### 8.2 Python 중심 권장 이유

문서 제작 도구는 코드 편집보다 파일 포맷 처리 비중이 높다.
Python은 PPTX, XLSX, DOCX, 이미지 처리 라이브러리가 안정적이다.

MVP에서는 MCP 서버와 로컬 파일 작업 실행기를 Python 프로세스 하나로 합친다.
이렇게 하면 원격 릴레이, 별도 세션 관리, 분리형 실행 계층의 연결 유지 로직 없이도 ChatGPT 연동 가능성을 빠르게 검증할 수 있다.

따라서 1차 구현은 Python MCP 서버 하나로 시작한다.
문서 품질 고도화와 템플릿 관리는 MCP 연결 검증 후 확장한다.

### 8.3 MVP 연결 방식: HTTPS 터널 기반 로컬 MCP 서버

MVP에서는 별도 원격 릴레이 서버를 운영하지 않는다.
사용자 PC에서 로컬 MCP 문서 서버를 실행하고, ngrok 또는 Cloudflare Tunnel로 HTTPS 주소를 생성한다.
ChatGPT 개발자 모드 커넥터에는 https://.../mcp 주소를 등록한다.

별도의 원격 릴레이 서버는 다음 조건이 생겼을 때 v2에서 검토한다.

- 항상 같은 고정 URL이 필요할 때
- 여러 PC를 연결해야 할 때
- 모바일 또는 외부 네트워크에서도 안정적으로 접속해야 할 때
- 사용자 계정, 인증, 장기 세션 관리가 필요할 때

### 8.4 추천 프로젝트 구조

```text
local-doc-agent/
 ├─ server/
 │   ├─ main.py                 # MCP 서버 진입점
 │   ├─ tools_files.py          # list/read/write/patch
 │   ├─ tools_docs.py           # markdown/docx/pptx/xlsx 생성
 │   ├─ tools_images.py         # 이미지 저장/삽입
 │   ├─ schemas.py              # Pydantic 입력 스키마
 │   ├─ config.py               # workspace root, port, 옵션
 │   └─ logging_utils.py        # JSONL 작업 로그
 ├─ workspace/
 │   ├─ docs/
 │   ├─ slides/
 │   ├─ assets/
 │   ├─ output/
 │   └─ backups/
 ├─ templates/
 │   ├─ planning_doc.md
 │   ├─ proposal_doc.md
 │   ├─ reference.docx
 │   └─ marp_theme.css
 ├─ logs/
 │   └─ operations.jsonl
 ├─ tests/
 │   ├─ test_files.py
 │   ├─ test_docs.py
 │   └─ test_paths.py
 ├─ pyproject.toml
 ├─ README.md
 └─ .env.example
```

### 8.5 추천 환경 변수

```env
LOCAL_DOC_AGENT_PORT=2091
LOCAL_DOC_AGENT_WORKSPACE=D:/LocalDocAgent/workspace
LOCAL_DOC_AGENT_LOGS=D:/LocalDocAgent/logs
LOCAL_DOC_AGENT_DEFAULT_OVERWRITE=true
LOCAL_DOC_AGENT_CREATE_BACKUP=true
LOCAL_DOC_AGENT_MAX_READ_CHARS=50000
```

## 9. UX 방향

### 9.1 목표 사용감

사용자는 웹 ChatGPT에 자연어로 요청한다.
ChatGPT는 필요할 때 MCP 도구를 호출한다.
사용자는 별도 문서 제작 프로그램을 직접 조작하지 않아도 된다.

목표 사용감:

- "이 기획서를 제안서 톤으로 고쳐줘"
- "이 내용을 PPT로 만들어줘"
- "방금 만든 이미지를 3번 슬라이드에 넣어줘"
- "일정표를 Excel로 정리해줘"
- "제안서와 발표 자료를 같이 만들어줘"

### 9.2 사용자에게 보여줄 결과

작업 완료 후 ChatGPT는 다음 정보를 제공한다.

- 생성 파일 경로
- 수정 파일 경로
- 백업 파일 경로
- diff 요약
- 오류 또는 추가 확인 필요 사항

예시:

```text
생성 파일:
- docs/game_proposal.md
- output/game_proposal.docx
- output/game_proposal.pptx
- output/development_schedule.xlsx

변경 요약:
- 제안서 목차 6개 섹션 구성
- 발표용 슬라이드 10장 생성
- 개발 일정표 12주 기준 작성

백업:
- backups/docs/game_proposal.20260507-153000.md
```

## 10. 개인용 파일 손상 방지 기준

본 프로젝트는 개인 로컬 작업용이므로 MVP에서는 인증·권한 관리보다 빠른 구현과 파일 손상 방지에 집중한다.

유지 기준:

- WORKSPACE_ROOT 하나만 지정
- 기본 작업은 workspace 내부에서 수행
- 기존 파일 덮어쓰기 전 자동 백업
- 작업 로그 JSONL 기록
- 삭제 도구는 MVP에서 제외
- 대용량 파일은 기본 제한
- 오류 발생 시 예외 메시지를 ChatGPT가 이해할 수 있게 반환

MVP에서 제외하는 항목:

- OAuth
- 사용자 계정 관리
- 다중 사용자 권한 관리
- 복잡한 인증 서버
- 운영용 원격 릴레이 보안 설계
- 과도한 denylist 정책
- 매번 수동 승인해야 하는 propose/commit 플로우

## 11. 개발 단계

개발 단계별로 ChatGPT 커넥터에 노출하는 도구 수를 제한한다.
각 단계에서 도구 호출이 안정화되면 다음 단계 도구를 추가한다.

### 11.0.1 현재 구현 상태

2026-05-07 기준 현재 상태:

- Git 저장소 초기화 완료
- 원격 저장소 `origin/main` 연결 완료
- FastMCP 기반 `/mcp` 서버 구현 완료
- 초기 노출 도구 5종 구현 완료
  - `ping`
  - `list_files`
  - `read_text_file`
  - `write_text_file`
  - `patch_text_file`
- 1단계 Markdown 도구 구현 완료
  - `create_markdown`
- workspace 외부 경로 차단 구현 완료
- 텍스트 확장자 제한 구현 완료
- 기존 파일 자동 백업 구현 완료
- diff summary 반환 구현 완료
- JSONL 작업 로그 구현 완료
- pytest 기준 로컬 테스트 통과
- ngrok HTTPS 터널 연결 완료
- ChatGPT 개발자 모드 커스텀 커넥터 등록 완료
- ChatGPT UI 기준 `ping` 호출 성공
- ChatGPT UI 기준 `list_files` 호출 성공
- ChatGPT UI 기준 `write_text_file` 호출 성공
- ChatGPT UI 기준 `patch_text_file` 호출 성공
- ChatGPT UI 기준 `create_markdown` 호출 성공
- ChatGPT UI 호출로 테스트 Markdown 파일 생성 및 수정 완료
- ChatGPT UI 호출로 구조화 Markdown 문서 생성 완료
- 기존 파일 수정 시 자동 백업 생성 확인 완료
- 작업 로그 및 오류 반환 기록 확인 완료
- 2단계 첫 기능 `export_docx_from_markdown` 구현 완료
- 로컬 MCP 클라이언트 기준 `export_docx_from_markdown` 도구 노출 확인 완료
- ChatGPT UI 기준 `export_docx_from_markdown` 호출 성공
- 2단계 기능 `create_xlsx_from_sheets` 구현 완료
- 로컬 MCP 클라이언트 기준 `create_xlsx_from_sheets` 도구 노출 및 호출 성공
- 2단계 기능 `create_pptx_from_spec` 구현 완료
- 로컬 MCP 클라이언트 기준 `create_pptx_from_spec` 도구 노출 및 호출 성공
- 3단계 기능 `list_assets`, `save_base64_image`, `insert_image_to_markdown` 구현 완료
- 로컬 MCP 클라이언트 기준 이미지 도구 3종 노출 및 호출 성공
- 3단계 기능 `insert_image_to_pptx` 구현 완료
- 로컬 MCP 클라이언트 기준 `insert_image_to_pptx` 도구 노출 및 호출 성공
- 유지보수 정리: 이미지 도구 구현을 `server/tools_assets.py`로 분리 완료
- 4단계 기능 `list_templates`, `create_markdown_from_template` 구현 완료
- 로컬 MCP 클라이언트 기준 템플릿 도구 2종 노출 및 호출 성공

미확정 항목:

- 쓰기 도구 반복 호출 시 권한 확인 모달 또는 제한 발생 패턴
- `create_markdown` 호출 시 섹션 목록이 누락되지 않도록 프롬프트 예시 보강 필요
- ChatGPT UI 기준 `create_xlsx_from_sheets` 호출 성공 여부
- ChatGPT UI 기준 `create_pptx_from_spec` 호출 성공 여부
- PPTX 템플릿, 폰트, 이미지 배치 품질 기준
- ChatGPT UI 기준 이미지 도구 4종 호출 성공 여부
- ChatGPT UI 기준 템플릿 도구 2종 호출 성공 여부

다음 우선 작업:

1. ChatGPT UI에서 `create_xlsx_from_sheets` 호출 확인
2. ChatGPT UI에서 `create_pptx_from_spec` 호출 확인
3. ChatGPT UI에서 이미지 도구 4종 호출 확인
4. ChatGPT UI에서 템플릿 도구 2종 호출 확인
5. 권한 제한 여부 기록
6. `create_markdown` 사용 예시 보강
7. DOCX/XLSX/PPTX 품질 기준 보강
8. 템플릿 기반 DOCX/PPTX 생성 착수 여부 결정

### 11.0 구현 시작 전 체크리스트

코드 구현을 시작하기 전에 아래 항목을 확인한다.

- Python 3.12+ 사용 가능 여부 확인
- uv 사용 여부 결정
- MCP Python SDK 또는 FastMCP 사용 방식 결정
- 로컬 서버 포트 결정: 기본값 2091
- workspace root 경로 결정
- ngrok 또는 Cloudflare Tunnel 중 하나 선택
- ChatGPT 개발자 모드에서 커스텀 커넥터 생성 화면 접근 가능 여부 확인
- /mcp URL 등록 방식 확인
- 초기 등록 도구를 ping, list_files, read_text_file, write_text_file, patch_text_file로 제한
- write 도구 실행 가능 여부를 0단계 완료 기준에 포함

### 11.1 0단계: MCP 연결 검증

목표:

- 로컬 Python MCP 서버 실행
- /mcp 엔드포인트 제공
- ngrok 또는 Cloudflare Tunnel로 HTTPS URL 생성
- ChatGPT 개발자 모드 커넥터에 등록
- ping, list_files, read_text_file 도구가 ChatGPT에서 보이는지 확인
- write_text_file 도구가 ChatGPT에서 보이는지 확인
- write_text_file 도구가 실제로 호출되는지 확인
- 쓰기 도구 호출 시 ChatGPT UI의 확인 모달 또는 권한 제한이 발생하는지 확인
- patch_text_file 도구가 보이고 호출 가능한지 확인

완료 기준:

- ChatGPT에서 도구 목록 확인 가능
- ChatGPT가 ping 호출 가능
- ChatGPT가 workspace 파일 목록 조회 가능
- ChatGPT가 테스트용 Markdown 파일을 workspace 내부에 생성 가능
- ChatGPT가 기존 테스트 Markdown 파일을 수정 가능
- 쓰기 도구가 막히는 경우, 읽기 전용 모드로 임시 전환 가능한지 판단

현재 판정:

- `ping`, `list_files`, `write_text_file`, `patch_text_file`, `create_markdown` 완료
- 자동 백업 생성 완료
- 작업 로그 기록 완료
- 0~1단계 MVP 완료 처리 가능

### 11.2 1단계: Markdown 파일 작업 MVP

목표:

- Markdown 문서 읽기·쓰기·수정 가능
- 기존 파일 덮어쓰기 시 자동 백업
- diff 요약 반환
- 작업 로그 기록

필수 기능:

- list_files
- read_text_file
- write_text_file
- patch_text_file
- create_markdown

현재 구현 상태:

- `create_markdown` 구현 완료
- 제목, 요약, 섹션 목록 기반 Markdown 생성 가능
- 저장, 덮어쓰기, 백업, diff summary 반환은 기존 텍스트 파일 도구 규칙 재사용
- 로컬 pytest 기준 통과
- ChatGPT UI 기준 호출 성공

### 11.3 2단계: 문서 변환 MVP

목표:

- Markdown을 DOCX, Marp deck, PPTX로 변환
- XLSX 신규 생성

필수 기능:

- export_docx_from_markdown
- create_marp_deck
- export_pptx_from_marp
- create_pptx_from_spec
- create_xlsx_from_sheets

선택 기능:

- extract_docx_text
- convert_docx_to_markdown

현재 구현 상태:

- `export_docx_from_markdown` 구현 완료
- Markdown 제목, 본문, bullet 목록을 DOCX 기본 스타일로 변환
- 출력 경로 workspace 내부 제한
- 기존 DOCX 덮어쓰기 시 백업 가능
- `create_xlsx_from_sheets` 구현 완료
- 시트 목록, 헤더, 행 데이터 기반 XLSX 신규 생성 가능
- 기존 XLSX 덮어쓰기 시 백업 가능
- `create_pptx_from_spec` 구현 완료
- 제목, 부제, 슬라이드 제목, 본문, 불릿, 노트 기반 PPTX 신규 생성 가능
- 기존 PPTX 덮어쓰기 시 백업 가능
- 로컬 pytest 기준 통과
- DOCX ChatGPT UI 호출 성공
- XLSX/PPTX ChatGPT UI 호출 검증 대기

### 11.4 3단계: 이미지 저장 및 삽입

목표:

- workspace/assets에 존재하는 이미지를 문서 생성 과정에서 안정적으로 참조
- 이미지 파일 저장
- Markdown에 이미지 링크 삽입
- PPTX 생성 시 이미지 포함

필수 기능:

- list_assets
- save_base64_image
- insert_image_to_markdown
- PPTX 생성 시 이미지 경로 지원

이미지 단계의 1차 목표는 ChatGPT 생성 이미지를 자동으로 저장하는 것이 아니라, workspace/assets에 존재하는 이미지를 문서 생성 과정에서 안정적으로 참조하는 것이다.

현재 구현 상태:

- `list_assets` 구현 완료
- `save_base64_image` 구현 완료
- `insert_image_to_markdown` 구현 완료
- `insert_image_to_pptx` 구현 완료
- base64 이미지 저장, assets 목록 조회, Markdown 이미지 링크 삽입 가능
- 기존 PPTX 지정 슬라이드에 이미지 삽입 가능
- 기존 Markdown 수정 시 백업 가능
- 기존 PPTX 수정 시 백업 가능
- 로컬 pytest 기준 통과
- 로컬 MCP 클라이언트 기준 호출 성공
- ChatGPT UI 호출 검증 대기

구조 정리:

- 이미지 도구 구현은 `server/tools_assets.py`에 배치
- 기존 MCP 등록 및 외부 도구명은 유지
- `server/tools_files.py`는 기존 도구 import 호환성을 유지

### 11.5 4단계: 템플릿과 작업 흐름 고도화

목표:

- 기획서, 제안서, 포트폴리오 템플릿 추가
- 문서 묶음 생성
- 반복 작업 자동화

필수 기능:

- templates/planning_doc.md
- templates/proposal_doc.md
- templates/reference.docx
- templates/marp_theme.css
- 결과물 묶음 생성 규칙

현재 구현 상태:

- `list_templates` 구현 완료
- `create_markdown_from_template` 구현 완료
- 내장 템플릿 3종 제공
  - `planning_doc`
  - `proposal_doc`
  - `checklist_doc`
- 템플릿 기반 Markdown 초안 생성 가능
- 기존 Markdown 덮어쓰기 시 백업 가능
- 로컬 pytest 기준 통과
- 로컬 MCP 클라이언트 기준 호출 성공
- ChatGPT UI 호출 검증 대기

### 11.6 5단계: 선택 확장 - 원격 릴레이 분리

목표:

- 항상 같은 URL 또는 여러 PC 연결이 필요해졌을 때 원격 릴레이 구조 검토

이 단계는 MVP에서 제외한다.

## 12. MVP 범위

### 12.1 포함

- 로컬 Python MCP 문서 서버
- HTTPS /mcp 엔드포인트
- ngrok 또는 Cloudflare Tunnel 연결
- ChatGPT 개발자 모드 커넥터 등록
- workspace root 설정
- 파일 목록 조회
- Markdown/TXT 읽기
- Markdown/TXT 생성 및 수정
- 기존 파일 덮어쓰기 시 자동 백업
- diff 요약 반환
- 작업 로그 JSONL 저장
- Markdown 기반 DOCX 변환
- Marp 기반 PPTX 생성
- 단순 spec 기반 PPTX 신규 생성
- XLSX 신규 생성
- assets 이미지 경로 참조
- base64 이미지 저장 보조 기능
- Markdown 이미지 삽입

### 12.2 제외

- 별도 원격 릴레이 서버
- OAuth 및 사용자 계정 관리
- 다중 사용자 권한 관리
- 별도 로컬 LLM
- 운영체제 명령 실행
- 임의 파일 삭제
- 기존 PPTX 정교한 수정
- 기존 XLSX 복잡한 수식 보존 수정
- PDF 정교한 편집
- 완전한 원격 데스크톱 기능
- 항상 켜져 있는 클라우드 서비스

### 12.3 선택 포함

- 기존 DOCX 텍스트 추출
- 기존 DOCX 기반 Markdown 초안 변환
- 기존 assets 이미지 목록 조회

## 13. 개발 우선순위

| 우선순위 | 기능 | 이유 |
| --- | --- | --- |
| 최상 | 로컬 MCP 서버 + /mcp 연결 검증 | ChatGPT에서 실제 도구 호출이 되는지 먼저 확인해야 함 |
| 최상 | list/read/write Markdown | 문서 작업의 핵심 루프 |
| 최상 | 자동 백업 + 작업 로그 | 개인용이라도 파일 손상 복구가 필요함 |
| 높음 | patch_text_file | 기존 기획서 수정에 필요 |
| 높음 | Markdown → DOCX | 제출용 문서 생성에 필요 |
| 높음 | Marp 기반 PPTX 생성 | 기획서 → 발표자료 흐름에 적합 |
| 높음 | XLSX 신규 생성 | 일정표, 체크리스트, 밸런스 표 제작에 필요 |
| 중간 | 기존 DOCX 텍스트 추출 | 기존 제출 문서나 참고 문서를 읽어 재작성하는 데 필요 |
| 중간 | DOCX → Markdown 변환 | 기존 Word 문서를 Markdown 원본 흐름으로 편입하기 위해 필요 |
| 중간 | 이미지 저장 및 Markdown 삽입 | 포트폴리오와 제안서 품질 향상 |
| 중간 | spec 기반 PPTX 생성 | 단순 슬라이드 자동 생성에 유용 |
| 중간 | 템플릿 관리 | 문서 톤과 구조 일관성 확보 |
| 낮음 | 기존 PPTX 수정 | 예외 처리가 많아 MVP 이후로 미룸 |
| 낮음 | 원격 릴레이 서버 | 개인용 MVP에서는 터널로 충분함 |
| 낮음 | PDF 편집 | 구현 복잡도 높음 |

## 14. 주요 리스크

### 14.1 ChatGPT 개발자 모드 정책 변화

개발자 모드, 커스텀 커넥터, MCP 앱, 쓰기 권한, 지원 전송 방식은 변경될 수 있다.
공식 문서 기준의 제약을 주기적으로 확인해야 한다.
특히 write_text_file과 patch_text_file은 사용 중인 계정, 워크스페이스, 앱 설정에 따라 확인 모달이 표시되거나 호출이 제한될 수 있다.
0단계에서 쓰기 도구의 실제 호출 가능 여부를 반드시 확인한다.

### 14.2 터널 연결 불안정

개인용 터널은 네트워크 상태, 방화벽, 터널 서비스 상태에 영향을 받는다.
MVP에서는 감수 가능하지만, 반복 사용 시 안정적인 터널 설정이 필요하다.

### 14.3 터널 URL 변경

ngrok 무료 URL이나 임시 터널은 재시작 시 주소가 바뀔 수 있다.
MVP에서는 감수하고, 자주 쓴다면 Cloudflare Tunnel 고정 도메인이나 유료 ngrok 고정 도메인을 검토한다.

### 14.4 도구 스키마가 너무 복잡해지는 문제

초기부터 많은 도구를 만들면 ChatGPT가 도구 선택을 헷갈릴 수 있다.
전체 MVP 기능은 파일 읽기, 쓰기, Markdown, DOCX, PPTX, XLSX 정도로 제한한다.
초기 커넥터 등록은 ping, list_files, read_text_file, write_text_file, patch_text_file 5개 도구로 시작한다.

대응:

- 0~1단계에서는 5개 도구만 노출
- 도구명은 명확하고 짧게 유지
- 각 도구 설명에 사용 시점과 제한을 명시
- 문서 변환 도구는 파일 작업 루프 검증 후 추가

### 14.5 PPTX 품질 편차

PPTX는 레이아웃, 폰트, 이미지 비율, 템플릿 호환성 문제가 발생하기 쉽다.
초기 목표는 완성본이 아니라 수정 가능한 초안 생성으로 둔다.

### 14.6 기존 문서 수정 난이도

기존 PPTX, XLSX, DOCX는 내부 구조가 복잡하다.
초기에는 기존 파일 정교한 수정보다 신규 생성과 단순 삽입 중심으로 접근한다.

### 14.7 파일 손상 위험

자동 수정 과정에서 기존 문서가 손상될 수 있다.
백업 생성, diff 요약, 작업 로그, workspace root 제한이 필요하다.

## 15. 완료 기준

1차 MVP 완료 기준:

- 로컬 Python MCP 문서 서버 실행 가능
- /mcp 엔드포인트 제공 가능
- ngrok 또는 Cloudflare Tunnel로 HTTPS URL 생성 가능
- ChatGPT 개발자 모드 커넥터에 등록 가능
- ChatGPT에서 도구 목록 확인 가능
- ChatGPT가 ping 도구 호출 가능
- ChatGPT가 workspace 파일 목록 조회 가능
- ChatGPT가 Markdown 파일 읽기 가능
- ChatGPT가 write_text_file 도구를 실제 호출해 테스트 파일을 생성 가능
- ChatGPT가 patch_text_file 도구를 실제 호출해 테스트 파일을 수정 가능
- 쓰기 도구 호출 시 발생하는 확인 모달 또는 권한 제한 여부가 기록됨
- ChatGPT가 Markdown 파일 생성 가능
- ChatGPT가 기존 Markdown 파일 수정 가능
- 기존 파일 덮어쓰기 시 백업 생성 가능
- 작업 로그가 JSONL로 기록됨
- ChatGPT가 Markdown 기반 DOCX 또는 PPTX 생성 요청 가능
- ChatGPT가 XLSX 생성 요청 가능
- 로컬 workspace/output 폴더에 결과 파일 저장 가능
- 작업 결과와 오류가 ChatGPT에 반환 가능

## 16. 최종 판단

사용자가 원하는 "웹 GPT가 내 컴퓨터 파일을 작업하는 느낌"은 개인용 MVP로 충분히 실현 가능하다.

다만 ChatGPT가 로컬 파일 시스템을 직접 탐색하는 방식이 아니라, 사용자가 실행한 로컬 MCP 문서 서버가 workspace 폴더 안에서 파일 작업을 수행하는 구조다.

MVP에서는 별도의 원격 릴레이 서버를 만들지 않는다.
사용자 PC에서 Python MCP 서버를 실행하고, HTTPS 터널로 /mcp 엔드포인트를 ChatGPT 개발자 모드 커넥터에 연결한다.

따라서 본 프로젝트의 1차 방향은 다음과 같다.

```text
로컬 AI 에이전트 개발이 아니라,
웹 ChatGPT용 개인 로컬 문서 작업 MCP 서버 개발.
```

핵심 가치는 웹 ChatGPT의 문서 작성 능력을 유지하면서, 결과물을 사용자의 로컬 workspace 폴더에 직접 생성·수정할 수 있게 만드는 데 있다.
