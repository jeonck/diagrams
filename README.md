# diagrams

제품 하나를 설계하며 만드는 다이어그램들을 **프로젝트 단위로** 모아 두는 저장소입니다.
공개 주소: **https://jeonck.github.io/diagrams/**

```
categories.json                그림 종류 분류 (전역)
phases.json                    설계 단계 (전역)
projects/
  order-platform/              온라인 상점 — 설계 완료
  notify-hub/                  알림 허브 — 설계 완료
    project.json               이름 · 한 줄 정의 · 상태 · 표시 순서(order)
    README.md                  프로젝트 브리프
    decisions/NNNN-....md      설계 결정 기록 (ADR)
    diagrams/<slug>/           meta.json · diagram.html · diagram.excalidraw
diagrams.json                  생성물 — 손으로 고치지 않습니다
index.html                     뷰어
tools/
  build-index.mjs              diagrams.json 과 README 표를 만든다
  check-freshness.mjs          낡았을 수 있는 그림을 찾는다
  generators/                  스펙 → diagram.html · diagram.excalidraw
```

다이어그램은 두 축으로 분류됩니다 — **언제 그리는가**(SDLC 단계)와 **무엇을 그리는가**(그림 종류).
뷰어에서 두 축을 토글할 수 있고, 목록 기본값은 SDLC 단계순입니다.
다이어그램과 ADR 은 나란히 있는 두 가지가 아니라 **번갈아 갑니다.**
요구·분석 그림으로 문제를 그려야 판단할 근거가 생기고, 결정을 내린 뒤에 그 결정을
설계·구현 그림으로 그립니다 — **그림 → 결정 → 그림**. 그래서 ADR 은 걸린 그림을
`basis`(판단의 근거로 본 그림)와 `diagrams`(이 결정이 만든 그림)로 나눠 적습니다.

## SDLC 단계

전체 SDLC를 압축한 네 단계입니다. 테스트와 유지보수는 이 저장소에서 다이어그램이 아니라
문서로 남기 때문에 단계로 두지 않았습니다.

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

두 프로젝트 모두 15개 대표 종류가 채워져 있습니다. 비어 있는 칸이 생기면
`node tools/build-index.mjs` 가 그 목록을 알려줍니다:

```
build-index: 알림 허브 에 아직 없는 산출물 10개 — 구조/클래스, 구조/컴포넌트, ...
```

각 프로젝트의 예제는 하나의 도메인을 소재로 삼아,
같은 시스템을 각도만 바꿔 본 그림이 되도록 했습니다 — 같은 도메인이 ERD 에서는 테이블로,
클래스 다이어그램에서는 책임과 합성으로, 상태 머신에서는 전이로 나타납니다.

## 다이어그램 목록

<!-- diagrams:start -->

프로젝트 2개 · 다이어그램 30개입니다.
이 표는 `node tools/build-index.mjs` 가 만들므로 직접 고치지 마세요.

### 온라인 상점

고객이 상품을 주문하고 결제하면, 재고를 차감하고 배송까지 이어지는 커머스 백엔드

`projects/order-platform/` · 설계 완료 · 다이어그램 15개 · 설계 결정 6개

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

### 알림 허브

다른 서비스가 보낸 이벤트를 받아 푸시·이메일·SMS로 내보내는 사내 공용 알림 플랫폼

`projects/notify-hub/` · 설계 완료 · 다이어그램 15개 · 설계 결정 3개

| 단계 | 종류 | 다이어그램 | 요약 |
| --- | --- | --- | --- |
| 요구 | 유스케이스 | [알림 허브 유스케이스](https://jeonck.github.io/diagrams/#notify-usecase/html) | 누가 이 서비스로 무엇을 하는가 |
| 요구 | BPMN | [실패 알림 처리 프로세스 (BPMN)](https://jeonck.github.io/diagrams/#notify-bpmn/html) | DLQ 로 넘어간 알림을 사람이 판단해 되살리거나 접는 과정 |
| 분석 | 클래스 | [알림 도메인 클래스](https://jeonck.github.io/diagrams/#notify-class/html) | 알림 한 건과 그것을 보내는 채널, 시도 기록의 관계 |
| 분석 | 상태 머신 | [알림 발송 상태 전이](https://jeonck.github.io/diagrams/#notify-state/html) | 알림 한 건이 접수되어 성공하거나 포기될 때까지 |
| 분석 | ERD | [알림 도메인 ERD](https://jeonck.github.io/diagrams/#notify-erd/html) | 수신자와 알림, 그리고 시도 기록이 놓이는 표 |
| 분석 | 데이터 흐름(DFD) | [알림 데이터 흐름 (레벨 1)](https://jeonck.github.io/diagrams/#notify-dfd/html) | 알림 데이터가 어떤 처리를 거쳐 어디에 쌓이는가 |
| 설계 | C4 컨텍스트·컨테이너 | [알림 허브 C4 컨텍스트·컨테이너](https://jeonck.github.io/diagrams/#notify-c4/html) | 시스템 경계 안의 컨테이너와, 경계 밖의 발신자·공급자 |
| 설계 | 컴포넌트 | [수신 API 컴포넌트](https://jeonck.github.io/diagrams/#notify-components/html) | 요청 하나가 수신 API 안에서 거치는 부품들 |
| 설계 | 시퀀스 | [알림 발송 시퀀스](https://jeonck.github.io/diagrams/#notify-sequence/html) | 요청 한 건이 접수되어 공급자에게 나가기까지, 그리고 중복이 걸러지는 지점 |
| 설계 | 액티비티 | [알림 발송 재시도 액티비티](https://jeonck.github.io/diagrams/#notify-activity/html) | 발송 워커 한 사이클 — 성공하거나, 백오프 뒤 다시 돌거나, 포기하거나 |
| 설계 | 패키지 | [모듈 의존 구조](https://jeonck.github.io/diagrams/#notify-packages/html) | 따로 배포되는 두 모듈이 하나의 도메인을 공유하는 방식 |
| 구현·운영 | 배포 | [알림 허브 배포 구성](https://jeonck.github.io/diagrams/#notify-deployment/html) | 큐를 사이에 두고 수신과 발송이 따로 확장되는 배치 |
| 구현·운영 | 네트워크 토폴로지 | [알림 허브 네트워크 토폴로지](https://jeonck.github.io/diagrams/#notify-network/html) | 어떤 서브넷에 무엇이 있고, 어디로 나가는가 |
| 구현·운영 | CI/CD 파이프라인 | [알림 허브 CI/CD 파이프라인](https://jeonck.github.io/diagrams/#notify-cicd/html) | 한 커밋에서 두 개의 배포 단위가 함께 나가는 경로 |
| 구현·운영 | 값 흐름 | [알림 한 건의 지연 분해](https://jeonck.github.io/diagrams/#notify-value-stream/html) | 요청이 접수되어 단말에 뜨기까지, 일한 시간과 기다린 시간 |

<!-- diagrams:end -->

## 설계 결정 (ADR)

`projects/<프로젝트>/decisions/NNNN-제목.md` 에 하나씩 둡니다. 파일 맨 앞에
`---` 로 감싼 **JSON 머리말**이 오고, 그 뒤가 본문입니다:

```
---
{
  "title": "세션을 Redis로 옮긴다",
  "status": "채택됨",
  "date": "2026-09-06",
  "phase": "operations",
  "supersedes": "0002-session-in-app-memory",
  "diagrams": ["deployment-topology"]
}
---

## 맥락
...
```

- `status` 는 `제안됨` · `채택됨` · `대체됨` · `폐기됨` 중 하나입니다. `대체됨` 이면
  `supersededBy` 를 반드시 적어야 합니다.
- `phase` 는 **이 결정을 내린 단계**입니다 (`phases.json` 의 id). 다이어그램과 같은 축에
  놓여, 뷰어의 SDLC 목록에서 그 단계의 그림들 **앞에** 나옵니다 — 결정하고 나서 그리기
  때문입니다. 그림 종류 축에서는 결정에 종류가 없으므로 사이드바 아래 묶음으로 돌아갑니다.
- `basis` 는 선택 사항입니다. **`basis` 와 `diagrams` 는 방향이 다릅니다.** `basis` 는 이 결정을 내릴 때 근거로 본
  그림이고, `diagrams` 는 이 결정이 만든 그림입니다. 같은 slug 를 양쪽에 적으면 빌드가
  실패합니다 — 근거인지 결과인지 하나를 골라야 합니다.

  | | 뜻 | 결정이 바뀌면 |
  |---|---|---|
  | `basis` | 판단의 근거로 본 그림 | 그대로 둡니다 |
  | `diagrams` | 이 결정이 만든 그림 | **따라 바꿔야 합니다** — 낡음 검사가 이쪽만 봅니다 |

  예: `0006 프로덕션 배포 직전에만 사람이 승인한다` 는 `주문 기능 값 흐름` 을 근거로
  (대기가 리드타임의 70%) 승인 게이트의 비용을 따졌고, 그 결정이 `CI/CD 파이프라인` 에
  승인 단계를 만들었습니다.
- 적은 slug 가 실제로 없으면 빌드가 실패합니다. 뷰어는 이 관계로 양방향 링크를 만듭니다 —
  결정 화면에는 `근거` · `결과` 로, 다이어그램 화면에는 `만든 결정` · `근거로 쓰인 결정` 으로
  나옵니다.
- **결정은 지우지 않습니다.** 틀린 결정도 상태만 `대체됨` 으로 바꾸고 남깁니다 —
  왜 그때 그렇게 판단했는지가 기록의 요점이기 때문입니다.

### 본문에 쓸 수 있는 것

뷰어는 마크다운 전체가 아니라 ADR 이 실제로 쓰는 만큼만 렌더링합니다. 의존성 없이
직접 처리하기 때문입니다.

| 쓸 수 있는 것 | 표기 |
|---|---|
| 제목 | `## 맥락` (1~4단계) |
| 문단 · 줄바꿈 | 빈 줄로 문단을 나눕니다 |
| 목록 | `- 불릿`, `1. 번호` |
| 표 | `\| 열 \| 열 \|` 아래에 `\|---\|---:\|` 구분선. `:---` `:---:` `---:` 로 정렬 |
| 이미지 | `![설명](assets/그림.png)` — 파일은 그 결정 폴더 아래 `assets/` 에 둡니다 |
| 코드 블록 | ``` 로 감싼 여러 줄 |
| 인용 | `> 인용문` |
| 강조 | `**굵게**` · `*기울임*` · `~~취소선~~` · `` `코드` `` |
| 링크 | `[글자](주소)`. `[0002](0002-....md)` 처럼 옆 ADR 을 가리키면 뷰어 안에서 열립니다 |
| 수평선 | `---` (머리말 구분선과 헷갈리지 않게 본문 안에서만) |

- 이미지 경로가 실제 파일을 가리키지 않으면 **빌드가 실패합니다.** 깨진 그림이
  배포된 뒤에 발견되는 일을 막습니다.
- 넓은 표는 좁은 화면에서 표 안에서만 가로로 흐릅니다. 본문은 밀리지 않습니다.
- 여기 없는 표기(각주 · 중첩 목록 · HTML 직접 삽입 등)는 그대로 글자로 나옵니다.

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
프로젝트가 둘 이상이면 뷰어 사이드바에 전환기가 생기고, 목록·태그·결정이 모두
선택한 프로젝트로 좁혀집니다. 표시 순서는 `project.json` 의 `order` 가 정합니다.
다이어그램 slug 는 프로젝트를 넘나들어 고유해야 하므로, 같은 종류를 여러 프로젝트에서
그릴 때는 `notify-state` 처럼 프로젝트를 접두어로 붙이면 편합니다.

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

`title` · `phase` · `category` · `kind` · `tags` · `summary` 는 필수, `updated`(YYYY-MM-DD)와
`order` · `sources` 는 선택입니다. `order` 는 같은 단계 안에서의 정렬에만 쓰이고, 단계와
카테고리 사이의 순서는 `phases.json` · `categories.json` 이 정합니다.

## 낡은 그림 찾기

문서 저장소의 진짜 비용은 그림을 그리는 일이 아니라, **그린 뒤에 세상이 바뀌었는데
그림만 그대로인 것**입니다. 두 가지를 자동으로 봅니다.

```sh
node tools/check-freshness.mjs            # 보고만 한다
node tools/check-freshness.mjs --strict   # 낡은 게 있으면 1 로 끝난다
```

- **결정보다 뒤처진 그림** — 그 결정이 **만든**(`diagrams`) 그림이 결정보다 오래되면
  알립니다. 근거로 본(`basis`) 그림은 세지 않습니다 — 결정이 바뀌어도 근거는 그대로입니다. 커밋된 날짜만 쓰므로 어디서 돌려도 결과가 같습니다. 뷰어에서도
  목록에 `!` 표시가 붙고, 상세 화면에 `결정 0003 이후 갱신 안 됨` 배지가 뜹니다.
- **코드보다 뒤처진 그림** — `meta.json` 에 `sources` 를 적어 두면, 그 경로가
  `updated` 이후에 바뀌었는지 git 로그로 봅니다.

```json
{
  "updated": "2026-09-09",
  "sources": ["src/order/**", "src/payment/PaymentGateway.java"]
}
```

배포 워크플로는 이 검사를 **막지 않고 알리기만** 합니다 (잡 요약에 표로 남습니다).
낡음은 "틀렸다" 가 아니라 "확인해 보라" 는 신호이기 때문입니다. 그림을 보고
고쳤거나 고칠 게 없었다면 `updated` 를 오늘 날짜로 바꾸면 신호가 꺼집니다.

이 저장소에는 애플리케이션 코드가 없어 `sources` 를 적은 그림이 아직 없습니다.
실제 코드 옆에 이 구조를 둘 때 쓰라고 만든 자리입니다.

폴더를 만든 뒤 목록을 다시 생성합니다:

```sh
node tools/build-index.mjs
```

`diagrams.json` 과 위 **다이어그램 목록 표는 생성물이므로 손으로 고치지 않습니다.**
CI가 `--check` 로 둘 다 다시 만들어 커밋본과 다르면 배포를 실패시키므로, 조용히 어긋날 일은 없습니다.

## 뷰어

[`index.html`](index.html) 이 `diagrams.json` 을 읽어 목록을 그립니다. 다이어그램을 추가할 때
뷰어 코드는 건드리지 않습니다.

- 프로젝트 브리프, **SDLC 단계 / 그림 종류 축 토글**, 검색(제목·요약·태그), 태그 필터, 갤러리 보기
- **SDLC 단계 축**에서는 결정이 그 단계의 그림들 앞에 놓여 `분석 · 0001 결정 · 그림들` 순서로 읽힙니다.
  그림 종류 축에서는 사이드바 아래에 **접힌 묶음**으로 들어갑니다
- 걸린 결정보다 오래된 그림은 목록에 `!` 표시가, 상세 화면에 **`결정 0003 이후 갱신 안 됨`** 배지가 붙습니다
- 비어 있는 카테고리는 "아직 없음" 으로 남아, 무엇을 아직 안 그렸는지 보입니다
- Excalidraw 버전이 없는 다이어그램은 탭이 “Excalidraw 없음”으로 바뀌고 비활성화됩니다
- 형식 전환: SVG/HTML 은 iframe 으로, Excalidraw 는 페이지에 내장된 간이 렌더러로
- 내려받기: 원본 `.html`, 스타일을 SVG 안에 넣어 재구성한 단독 `.svg`, 그리고 `.excalidraw`
- URL 해시로 바로 열기 — `#mvc-structure/html`, `#mvc-sequence/excalidraw`, `#gallery`, `#decision/0005-session-in-redis`
- `/` 키로 검색창 포커스, 왼쪽 위 **Diagrams** 를 누르면 첫 화면으로
- **좁은 화면**에서는 목록이 서랍으로 들어가고 다이어그램이 첫 화면을 차지합니다.
  액자 높이는 그림에 맞춰지고, **확대 / 맞춤** 토글로 원래 크기로 보며 좌우로 밀 수 있습니다

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

`main` 에 푸시하면 [`.github/workflows/pages.yml`](.github/workflows/pages.yml) 이 세 가지를
검사한 뒤 GitHub Pages 로 배포합니다. `.claude/` 와 `tools/` 는 사이트에 포함되지 않습니다.

| 검사 | 잡는 것 | 배포를 막나 |
|---|---|---|
| `node tools/build-index.mjs --check` | `meta.json` ↔ `diagrams.json` ↔ README 표가 어긋남 | 예 |
| `python3 tools/generators/build.py --check` | 스펙 ↔ 그림 파일이 어긋남 | 예 |
| `node tools/check-freshness.mjs` | 결정·코드보다 뒤처진 그림 | 아니오 (잡 요약에 표로 남깁니다) |

앞의 둘은 **생성물이 조용히 어긋나는 것**을 막고, 마지막 하나는 **그림이 조용히 낡는 것**을
알립니다. 낡음은 틀렸다는 뜻이 아니라 확인해 보라는 신호라서 배포는 막지 않습니다.

## 개선 기록

한 장짜리 MVC 다이어그램에서 시작해 여기까지 왔습니다. 무엇을 왜 바꿨는지 남깁니다.

### 뼈대 — 그림 한 장에서 설계 자료실로

| 무엇을 | 왜 |
|---|---|
| 매니페스트(`diagrams.json`) 기반 뷰어 | 뷰어가 모든 경로를 목록에서 읽게 했습니다. 덕분에 뒤에 폴더 구조를 통째로 바꿀 때 **뷰어 코드는 한 줄도 안 바뀌었습니다** |
| 두 축 분류 — SDLC 단계 · 그림 종류 | "언제 그리는가" 와 "무엇을 그리는가" 는 다른 질문입니다. 한 축으로는 둘 중 하나를 잃습니다 |
| 대표 15종 채우기 | 빈 카테고리를 "아직 없음" 으로 남겨 무엇을 안 그렸는지 보이게 하고, 그 목록을 다 채웠습니다 |
| 프로젝트 계층 (`projects/<이름>/`) | 실무에서 다이어그램은 제품 하나를 설계하며 나옵니다. 프로젝트가 빠지면 그림이 공중에 뜹니다 |
| 설계 결정(ADR) + 양방향 링크 | 그림만으로는 "왜 이렇게 됐는지" 가 남지 않습니다. ADR 0003 을 결론 내자 다이어그램 3장이 따라 바뀌었는데, 그 연결을 만들어 두지 않았다면 놓쳤을 변경입니다 |
| 두 번째 프로젝트 (알림 허브) | 프로젝트가 하나일 때는 안 보이던 가정들이 드러났습니다 (slug 충돌, 프로젝트별 필터) |
| README 표 자동 생성 | 손으로 관리하는 목록은 반드시 어긋납니다. CI 가 다시 만들어 비교합니다 |

### 뷰어 — 화면을 실제로 쓸 수 있게

| 무엇을 | 왜 |
|---|---|
| 설계 결정 목록을 접었습니다 | 6건이 사이드바 아래 34vh 를 고정으로 차지해 정작 주인공인 다이어그램 목록이 밀렸습니다 |
| 왼쪽 위 **Diagrams** = 홈 | 검색·태그·결정·보기 방식을 한 번에 풀 방법이 없었습니다 |
| 모바일에서 다이어그램을 첫 화면으로 | 좁은 화면에서 검색·태그·목록이 한 화면을 다 쓰고 그림은 스크롤 아래에 숨어 있었습니다. 목록을 서랍으로 넣고, 액자 높이를 그림에 맞췄습니다 |
| 확대 / 맞춤 토글 | 폭에 맞춰 줄인 그림은 글자가 너무 작습니다. 원래 크기로 보고 좌우로 밀 수 있게 했습니다 |
| 낡음 배지 · `!` 표시 | 걸린 결정보다 오래된 그림을 화면에서 바로 알아보게 했습니다 |

### 흐름 — 결정과 그림의 순서를 담다

> "실제 업무 진행으로 보면 ADR 을 결정한 후에 설계를 진행하는 것 아닐까?"

절반은 맞고, 그 절반이 구조의 결함을 가리켰습니다. **결정하려면 먼저 문제를 그려야 하고
(요구·분석), 결정한 뒤에 그 결정을 그립니다(설계·구현).** 그림 → 결정 → 그림입니다.

확인해 보니 ADR **본문은 이미 두 역할을 구분해 쓰고 있었습니다.**

- `0001` — "`주문 상태 전이` 다이어그램이 **이 결정의 표를 그대로 그린 것**" → 결과
- `0006` — "치르는 대가 … **`주문 기능 값 흐름` 에서 보듯** 대기가 리드타임의 대부분" → 근거

그런데 머리말은 `diagrams` 한 칸뿐이라 둘이 뭉뚱그려져 있었습니다. 세 가지를 고쳤습니다.

| 무엇을 | 왜 |
|---|---|
| `basis` / `diagrams` 로 링크를 나눔 | `basis` 는 판단의 근거로 본 그림, `diagrams` 는 이 결정이 만든 그림입니다. 같은 slug 를 양쪽에 적으면 빌드가 실패합니다 |
| 낡음 검사가 결과 쪽만 보게 | 결정이 바뀌어도 근거는 그대로입니다. `0006` 날짜를 미래로 두면 `cicd-pipeline` 만 잡히고 `value-stream` 은 안 잡힙니다 — 고치기 전이라면 둘 다 잡혔을 자리입니다 |
| ADR 에 `phase` 를 주어 SDLC 축에 올림 | 목록이 `분석 · 0001 주문을 상태 기계로 다룬다 · 주문 도메인 클래스 …` 순서로 읽힙니다. 그림 종류 축에서는 결정에 종류가 없으므로 아래 묶음으로 돌아갑니다 |

기존 링크 19건 중 **재분류된 것은 `0006 → value-stream` 한 건**입니다. 나머지는 본문을
다시 읽어봐도 모두 결과 쪽이었습니다. 기존 결정 9건의 단계는 요구 0 · 분석 1 · 설계 4 ·
구현·운영 4 로, **요구 단계 결정은 없는 대로 뒀습니다.**

### 만들고 지키는 장치 — 유지보수 비용 줄이기

지적받은 세 가지 단점 중 앞의 둘을 처리했습니다.

**1. 수동 작성·유지보수 비용**

- 그림 파일은 손으로 쓴 SVG 180줄이 아니라 **스펙에서 나옵니다.** 그런데 그 생성기가
  저장소 밖에 있었습니다. 안으로 들여오고, 스펙 한 장 = 파일 한 개로 나누고,
  생성기가 산출물을 읽던 순환 의존을 끊고, 생성기가 없던 5장까지 옮겼습니다.
  → **30장 × 2포맷 = 60개 파일이 전부 스펙에서 나옵니다.** 색·글꼴·여백은 템플릿 한 곳입니다.
- `build.py --check` 가 배포 전에 스펙과 산출물을 비교합니다. `diagram.html` 을 손으로
  고치면 배포가 실패합니다.
- **낡음 검사** — 그 결정이 **만든** 그림이 결정보다 오래됐거나(git 없이 날짜만으로),
  `meta.json` 의 `sources` 에 적은 코드가 `updated` 이후에 바뀌었으면 알립니다.
  근거로 본 그림은 세지 않습니다.

**2. 포맷 한계**

- ADR 본문에 **표 · 이미지 · 코드 블록 · 번호 목록 · 인용문 · 수평선**을 쓸 수 있습니다.
  CDN 이 막힌 환경이라 파서를 못 받아 직접 짠 부분집합이었지, 설계상의 제약은 아니었습니다.
- 본문이 가리키는 이미지가 없으면 **빌드가 실패합니다.**

**3. 확장성 — 지금은 하지 않습니다**

인덱스가 다이어그램 1장당 약 930바이트(지금 30장 + ADR 9건에 28KB)라 **450장이어도 420KB** 로,
정적 페이지 한 번 fetch 로 충분합니다.
먼저 무너지는 것은 용량이 아니라 소유권(저장소 하나 = PR 큐 하나)이므로, **프로젝트가 5개를
넘을 때** 각 저장소의 인덱스 조각을 합치는 연합 구조로 갑니다. 뷰어가 모든 경로를
매니페스트에서 읽으므로 그때도 뷰어는 바뀌지 않습니다.

### 환경 때문에 이렇게 된 것

- **Excalidraw 렌더러를 직접 짰습니다** — 이 저장소를 만든 환경에서 모든 CDN 이 막혀
  공식 `@excalidraw/excalidraw` 를 쓸 수 없었습니다. 손그림 질감과 Virgil 글꼴이 없는
  간이 렌더러입니다. 원본 `.excalidraw` 파일은 excalidraw.com 에서 그대로 열립니다.
- **마크다운 파서도 직접 짰습니다** — 같은 이유입니다. 그래서 위의 표기만 지원합니다.
