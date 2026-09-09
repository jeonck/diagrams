# diagrams

제품 하나를 설계하며 만드는 다이어그램들을 **프로젝트 단위로** 모아 두는 저장소입니다.
공개 주소: **https://jeonck.github.io/diagrams/**

```
categories.json                그림 종류 분류 (전역)
phases.json                    설계 단계 (전역)
projects/
  order-platform/
    project.json               프로젝트 이름 · 한 줄 정의 · 상태
    README.md                  프로젝트 브리프
    diagrams/<slug>/           meta.json · diagram.html · diagram.excalidraw
diagrams.json                  생성물
index.html                     뷰어
```

다이어그램은 두 축으로 분류됩니다 — **언제 그리는가**(설계 단계)와 **무엇을 그리는가**(그림 종류).
뷰어에서 두 축을 토글할 수 있고, 목록 기본값은 설계 단계순입니다.

## 설계 단계

| id | 단계 | 답하는 질문 |
| --- | --- | --- |
| `requirements` | 요구 | 무엇을, 왜 만드는가 |
| `analysis` | 분석 | 문제 영역을 어떻게 이해했는가 |
| `design` | 설계 | 어떻게 만들 것인가 |
| `operations` | 구현·운영 | 어디서 돌리고, 어떻게 내보내는가 |

## 카테고리

그림의 종류입니다. UML 2.5의 구조/행위 구분에 실무에서 함께 쓰이는 표준(C4·ERD·DFD·BPMN)을
얹은 분류이고, 목록과 순서는 [`categories.json`](categories.json)이 정합니다.

| id | 카테고리 | 답하는 질문 | 대표 종류 |
| --- | --- | --- | --- |
| `structure` | 구조 | 시스템이 무엇으로 이루어져 있는가 | 클래스 · 컴포넌트 · 패키지 · C4 컨텍스트·컨테이너 |
| `behavior` | 행위 | 시간에 따라 무엇이 일어나는가 | 시퀀스 · 상태 머신 · 액티비티 · 유스케이스 |
| `data` | 데이터 | 데이터가 어떤 모양이고 어디로 흐르는가 | ERD · 데이터 흐름(DFD) |
| `deployment` | 배포·인프라 | 어디서 어떻게 돌아가는가 | 배포 · 네트워크 토폴로지 |
| `process` | 프로세스 | 일이 사람과 시스템 사이를 어떻게 흐르는가 | BPMN · CI/CD 파이프라인 · 값 흐름 |

`meta.json` 의 `category` 와 `kind` 는 각각 이 표의 `id` 와 대표 종류 중 하나여야 하고,
아니면 `build-index` 가 실패합니다. **프로젝트에 아직 없는 종류는 빌드가 알려줍니다** —
남은 설계 산출물 체크리스트인 셈입니다.

```
$ node tools/build-index.mjs
build-index: diagrams.json 갱신 (15개)
```

현재 15개 대표 종류가 모두 채워져 있습니다. 예제는 모두 같은 주문 도메인을 소재로 삼아,
같은 시스템을 각도만 바꿔 본 그림이 되도록 했습니다 — 같은 도메인이 ERD 에서는 테이블로,
클래스 다이어그램에서는 책임과 합성으로, 상태 머신에서는 전이로 나타납니다.

## 다이어그램 목록

<!-- diagrams:start -->

**온라인 상점** — 고객이 상품을 주문하고 결제하면, 재고를 차감하고 배송까지 이어지는 커머스 백엔드

설계 단계순으로 15개입니다. 파일은 `projects/<프로젝트>/diagrams/<slug>/` 에 있고,
이 표는 `node tools/build-index.mjs` 가 만들므로 직접 고치지 마세요.

| 단계 | 종류 | 다이어그램 | 요약 |
| --- | --- | --- | --- |
| 요구 | 유스케이스 | [쇼핑몰 유스케이스](https://jeonck.github.io/diagrams/#shop-usecase/html) | 누가 이 시스템으로 무엇을 할 수 있는가 |
| 요구 | BPMN | [주문 이행 프로세스 (BPMN)](https://jeonck.github.io/diagrams/#fulfillment-bpmn/html) | 주문 한 건이 부서를 넘나들며 처리되는 순서 |
| 분석 | 클래스 | [주문 도메인 클래스](https://jeonck.github.io/diagrams/#order-class/html) | 같은 도메인을 데이터가 아니라 책임과 관계로 본 그림 |
| 분석 | ERD | [주문 도메인 ERD](https://jeonck.github.io/diagrams/#order-erd/html) | 고객이 주문을 내고, 주문이 항목과 결제로 갈라지는 관계 |
| 분석 | 상태 머신 | [주문 상태 전이](https://jeonck.github.io/diagrams/#order-state/html) | 주문 한 건이 가질 수 있는 상태와, 상태를 바꾸는 사건 |
| 분석 | 데이터 흐름(DFD) | [주문 데이터 흐름 (레벨 1)](https://jeonck.github.io/diagrams/#order-dfd/html) | 주문 데이터가 어떤 처리를 거쳐 어디에 쌓이는가 |
| 설계 | C4 컨텍스트·컨테이너 | [C4 컨텍스트·컨테이너](https://jeonck.github.io/diagrams/#c4-container/html) | 시스템 경계 안의 컨테이너와, 경계 밖의 사람·외부 시스템 |
| 설계 | 패키지 | [패키지 의존 구조](https://jeonck.github.io/diagrams/#package-deps/html) | 어느 패키지가 어느 패키지를 알아도 되는가 |
| 설계 | 컴포넌트 | [MVC 구조](https://jeonck.github.io/diagrams/#mvc-structure/html) | Model·View·Controller 세 역할과 그 사이의 의존 방향 |
| 설계 | 시퀀스 | [MVC 요청 시퀀스](https://jeonck.github.io/diagrams/#mvc-sequence/html) | 주문 생성 요청 한 건이 각 역할을 거쳐 응답으로 돌아오기까지 |
| 설계 | 액티비티 | [결제 처리 액티비티](https://jeonck.github.io/diagrams/#checkout-activity/html) | 장바구니에서 확인 메일까지, 분기와 병렬이 있는 처리 흐름 |
| 구현·운영 | 배포 | [웹 서비스 배포 구성](https://jeonck.github.io/diagrams/#deployment-topology/html) | 요청이 엣지를 지나 앱 계층에 닿고, 읽기와 쓰기가 갈라지는 지점 |
| 구현·운영 | 네트워크 토폴로지 | [네트워크 토폴로지](https://jeonck.github.io/diagrams/#network-topology/html) | 어떤 서브넷에 무엇이 있고, 어느 포트로 통하는가 |
| 구현·운영 | CI/CD 파이프라인 | [CI/CD 파이프라인](https://jeonck.github.io/diagrams/#cicd-pipeline/html) | 커밋 한 번이 프로덕션에 닿기까지 거치는 관문 |
| 구현·운영 | 값 흐름 | [주문 기능 값 흐름](https://jeonck.github.io/diagrams/#value-stream/html) | 요구 하나가 배포되기까지, 일한 시간과 기다린 시간 |

<!-- diagrams:end -->

## 다이어그램 추가하기

다이어그램 하나가 폴더 하나입니다. 폴더 이름이 곧 slug이고, 뷰어 URL의 해시이기도 하며,
프로젝트를 넘나들어 고유해야 합니다.

```
projects/<프로젝트>/diagrams/<slug>/
  meta.json            제목·단계·종류·태그·요약
  diagram.html         SVG/HTML (필수)
  diagram.excalidraw   편집 가능한 버전 (선택)
```

새 프로젝트는 `projects/<이름>/` 아래에 `project.json` 과 `diagrams/` 를 만들면 됩니다.

`meta.json`:

```json
{
  "title": "MVC 구조",
  "phase": "design",
  "category": "structure",
  "kind": "컴포넌트",
  "tags": ["패턴", "컴포넌트"],
  "summary": "Model·View·Controller 세 역할과 그 사이의 의존 방향",
  "updated": "2026-09-09",
  "order": 30
}
```

`title` · `phase` · `category` · `kind` · `tags` · `summary` 는 필수, `updated`(YYYY-MM-DD)와 `order` 는 선택입니다.
`order` 는 같은 단계 안에서의 정렬에만 쓰이고, 단계와 카테고리 사이의 순서는
`phases.json` · `categories.json` 이 정합니다.

폴더를 만든 뒤 목록을 다시 생성합니다:

```sh
node tools/build-index.mjs
```

`diagrams.json` 과 위 **다이어그램 목록 표는 생성물이므로 손으로 고치지 않습니다.**
CI가 `--check` 로 둘 다 다시 만들어 커밋본과 다르면 배포를 실패시키므로, 조용히 어긋날 일은 없습니다.

## 뷰어

[`index.html`](index.html) 이 `diagrams.json` 을 읽어 목록을 그립니다. 다이어그램을 추가할 때
뷰어 코드는 건드리지 않습니다.

- 프로젝트 브리프, **설계 단계 / 그림 종류 축 토글**, 검색(제목·요약·태그), 태그 필터, 갤러리 보기
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
