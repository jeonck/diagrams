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

현재 15개 대표 종류가 모두 채워져 있습니다. 예제는 모두 같은 주문 도메인을 소재로 삼아,
같은 시스템을 각도만 바꿔 본 그림이 되도록 했습니다 — 같은 도메인이 ERD 에서는 테이블로,
클래스 다이어그램에서는 책임과 합성으로, 상태 머신에서는 전이로 나타납니다.

## 다이어그램 목록

<!-- diagrams:start -->

현재 15개입니다. 파일은 `diagrams/<slug>/` 에 있고, 이 표는
`node tools/build-index.mjs` 가 만들므로 직접 고치지 마세요.

| 카테고리 | 종류 | 다이어그램 | 요약 |
| --- | --- | --- | --- |
| 구조 | 컴포넌트 | [MVC 구조](https://jeonck.github.io/diagrams/#mvc-structure/html) | Model·View·Controller 세 역할과 그 사이의 의존 방향 |
| 구조 | 클래스 | [주문 도메인 클래스](https://jeonck.github.io/diagrams/#order-class/html) | 같은 도메인을 데이터가 아니라 책임과 관계로 본 그림 |
| 구조 | 패키지 | [패키지 의존 구조](https://jeonck.github.io/diagrams/#package-deps/html) | 어느 패키지가 어느 패키지를 알아도 되는가 |
| 구조 | C4 컨텍스트·컨테이너 | [C4 컨텍스트·컨테이너](https://jeonck.github.io/diagrams/#c4-container/html) | 시스템 경계 안의 컨테이너와, 경계 밖의 사람·외부 시스템 |
| 행위 | 시퀀스 | [MVC 요청 시퀀스](https://jeonck.github.io/diagrams/#mvc-sequence/html) | 주문 생성 요청 한 건이 각 역할을 거쳐 응답으로 돌아오기까지 |
| 행위 | 상태 머신 | [주문 상태 전이](https://jeonck.github.io/diagrams/#order-state/html) | 주문 한 건이 가질 수 있는 상태와, 상태를 바꾸는 사건 |
| 행위 | 액티비티 | [결제 처리 액티비티](https://jeonck.github.io/diagrams/#checkout-activity/html) | 장바구니에서 확인 메일까지, 분기와 병렬이 있는 처리 흐름 |
| 행위 | 유스케이스 | [쇼핑몰 유스케이스](https://jeonck.github.io/diagrams/#shop-usecase/html) | 누가 이 시스템으로 무엇을 할 수 있는가 |
| 데이터 | ERD | [주문 도메인 ERD](https://jeonck.github.io/diagrams/#order-erd/html) | 고객이 주문을 내고, 주문이 항목과 결제로 갈라지는 관계 |
| 데이터 | 데이터 흐름(DFD) | [주문 데이터 흐름 (레벨 1)](https://jeonck.github.io/diagrams/#order-dfd/html) | 주문 데이터가 어떤 처리를 거쳐 어디에 쌓이는가 |
| 배포·인프라 | 배포 | [웹 서비스 배포 구성](https://jeonck.github.io/diagrams/#deployment-topology/html) | 요청이 엣지를 지나 앱 계층에 닿고, 읽기와 쓰기가 갈라지는 지점 |
| 배포·인프라 | 네트워크 토폴로지 | [네트워크 토폴로지](https://jeonck.github.io/diagrams/#network-topology/html) | 어떤 서브넷에 무엇이 있고, 어느 포트로 통하는가 |
| 프로세스 | CI/CD 파이프라인 | [CI/CD 파이프라인](https://jeonck.github.io/diagrams/#cicd-pipeline/html) | 커밋 한 번이 프로덕션에 닿기까지 거치는 관문 |
| 프로세스 | BPMN | [주문 이행 프로세스 (BPMN)](https://jeonck.github.io/diagrams/#fulfillment-bpmn/html) | 주문 한 건이 부서를 넘나들며 처리되는 순서 |
| 프로세스 | 값 흐름 | [주문 기능 값 흐름](https://jeonck.github.io/diagrams/#value-stream/html) | 요구 하나가 배포되기까지, 일한 시간과 기다린 시간 |

<!-- diagrams:end -->

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

`diagrams.json` 과 위 **다이어그램 목록 표는 생성물이므로 손으로 고치지 않습니다.**
CI가 `--check` 로 둘 다 다시 만들어 커밋본과 다르면 배포를 실패시키므로, 조용히 어긋날 일은 없습니다.

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
