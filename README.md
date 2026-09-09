# diagrams

다이어그램 모음. 공개 주소: **https://jeonck.github.io/diagrams/**

## 다이어그램 추가하기

다이어그램 하나가 폴더 하나입니다. 폴더 이름이 곧 slug이고, 뷰어 URL의 해시이기도 합니다.

```
diagrams/<slug>/
  meta.json            제목·묶음·태그·요약
  diagram.html         SVG/HTML (필수)
  diagram.excalidraw   편집 가능한 버전 (선택)
```

`meta.json`:

```json
{
  "title": "MVC 구조",
  "group": "아키텍처 패턴",
  "tags": ["패턴", "구조"],
  "summary": "Model·View·Controller 세 역할과 그 사이의 의존 방향",
  "updated": "2026-09-09",
  "order": 1
}
```

`title` · `group` · `tags` · `summary` 는 필수, `updated`(YYYY-MM-DD)와 `order` 는 선택입니다.
묶음은 그 안에서 `order` 가 가장 앞선 다이어그램 순으로 정렬됩니다.

폴더를 만든 뒤 목록을 다시 생성합니다:

```sh
node tools/build-index.mjs
```

`diagrams.json` 은 **생성물이므로 손으로 고치지 않습니다.** CI가 `--check` 로 다시 만들어
커밋본과 다르면 배포를 실패시키므로, 목록이 조용히 어긋날 일은 없습니다.

## 뷰어

[`index.html`](index.html) 이 `diagrams.json` 을 읽어 목록을 그립니다. 다이어그램을 추가할 때
뷰어 코드는 건드리지 않습니다.

- 검색(제목·요약·태그), 태그 필터, 묶음별 목록, 갤러리 보기
- 형식 전환: SVG/HTML 은 iframe 으로, Excalidraw 는 페이지에 내장된 간이 렌더러로
- 내려받기: 원본 `.html`, 스타일을 SVG 안에 넣어 재구성한 단독 `.svg`, 그리고 `.excalidraw`
- URL 해시로 바로 열기 — `#mvc-structure/html`, `#mvc-sequence/excalidraw`, `#gallery`
- `/` 키로 검색창 포커스

외부 스크립트·CDN을 전혀 쓰지 않습니다. 다만 `diagrams.json` 과 Excalidraw 파일을 `fetch` 로
읽기 때문에 `file://` 로 직접 열면 동작하지 않습니다:

```sh
python3 -m http.server        # http://localhost:8000
```

## 그리기

[`.claude/skills/diagram-maker/`](.claude/skills/diagram-maker) 에
[openclaw/openclaw](https://github.com/openclaw/openclaw) 의 `diagram-maker` 스킬(MIT)이 들어 있어,
이 저장소에서 작업하는 Claude Code 세션이 자동으로 사용합니다. 개인 환경 전체에서 쓰려면:

```sh
cp -r .claude/skills/diagram-maker ~/.claude/skills/
```

## 배포

`main` 에 푸시하면 [`.github/workflows/pages.yml`](.github/workflows/pages.yml) 이 목록 최신성을
검사한 뒤 GitHub Pages 로 배포합니다. `.claude/` 와 `tools/` 는 사이트에 포함되지 않습니다.
