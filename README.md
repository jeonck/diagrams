# diagrams

다이어그램 모음. 공개 주소: **https://jeonck.github.io/diagrams/**

## 카테고리

다이어그램 종류를 기준으로 다섯 칸으로 나눕니다. UML 2.5의 구조/행위 구분에 실무에서 함께 쓰이는
표준(C4·ERD·DFD·BPMN)을 얹은 분류입니다. 목록과 순서는
[`diagrams/categories.json`](diagrams/categories.json)이 정합니다.

| id | 카테고리 | 답하는 질문 | 대표 종류 |
| --- | --- | --- | --- |
| `structure` | 구조 | 시스템이 무엇으로 이루어져 있는가 | 클래스 · 컴포넌트 · 패키지 · C4 컨텍스트·컨테이너 |
| `behavior` | 행위 | 시간에 따라 무엇이 일어나는가 | 시퀀스 · 상태 머신 · 액티비티 · 유스케이스 |
| `data` | 데이터 | 데이터가 어떤 모양이고 어디로 흐르는가 | ERD · 데이터 흐름(DFD) |
| `deployment` | 배포·인프라 | 어디서 어떻게 돌아가는가 | 배포 · 네트워크 토폴로지 |
| `process` | 프로세스 | 일이 사람과 시스템 사이를 어떻게 흐르는가 | BPMN · CI/CD 파이프라인 · 값 흐름 |

`meta.json` 의 `category` 와 `kind` 는 각각 이 표의 `id` 와 대표 종류 중 하나여야 하고,
아니면 `build-index` 가 실패합니다. 아직 그리지 않은 대표 종류가 있으면 빌드가 그 목록을
알려주므로, 무엇이 비어 있는지 눈으로 대조할 필요가 없습니다.

```
$ node tools/build-index.mjs
build-index: diagrams.json 갱신 (15개)
```

현재 15개 대표 종류가 모두 채워져 있고, 예제는 모두 같은 주문 도메인을 소재로 삼아
같은 시스템을 다른 각도에서 본 그림이 되도록 했습니다.

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
  "category": "structure",
  "kind": "컴포넌트",
  "tags": ["패턴", "컴포넌트"],
  "summary": "Model·View·Controller 세 역할과 그 사이의 의존 방향",
  "updated": "2026-09-09",
  "order": 10
}
```

`title` · `category` · `kind` · `tags` · `summary` 는 필수, `updated`(YYYY-MM-DD)와 `order` 는 선택입니다.
`order` 는 같은 카테고리 안에서의 정렬에만 쓰이고, 카테고리 사이의 순서는 `categories.json` 이 정합니다.

폴더를 만든 뒤 목록을 다시 생성합니다:

```sh
node tools/build-index.mjs
```

`diagrams.json` 은 **생성물이므로 손으로 고치지 않습니다.** CI가 `--check` 로 다시 만들어
커밋본과 다르면 배포를 실패시키므로, 목록이 조용히 어긋날 일은 없습니다.

## 뷰어

[`index.html`](index.html) 이 `diagrams.json` 을 읽어 목록을 그립니다. 다이어그램을 추가할 때
뷰어 코드는 건드리지 않습니다.

- 검색(제목·요약·태그), 태그 필터(기본 8개, 나머지는 펼치기), 카테고리별 목록, 갤러리 보기
- 비어 있는 카테고리는 "아직 없음" 으로 남아, 무엇을 아직 안 그렸는지 보입니다
- Excalidraw 버전이 없는 다이어그램은 탭이 “Excalidraw 없음”으로 바뀌고 비활성화됩니다
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
