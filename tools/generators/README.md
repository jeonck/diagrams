# 다이어그램 생성기

`projects/*/diagrams/*/diagram.html` 과 `diagram.excalidraw` 는 **손으로 쓰지 않습니다.**
`specs/` 의 스펙 한 장이 두 포맷을 함께 찍어냅니다.

```sh
python3 tools/generators/build.py                # 30장 전부 다시 생성
python3 tools/generators/build.py order-class    # 한 장만
python3 tools/generators/build.py --check        # 커밋본과 같은지 확인 (파일을 건드리지 않음)
```

`--check` 는 배포 워크플로에서 돌아갑니다. **`diagram.html` 을 손으로 고치면 배포가 실패합니다** —
고칠 곳은 스펙입니다.

## 폴더

```
tools/generators/
  build.py              러너 — 스펙을 돌리고, --check 로 커밋본과 비교한다
  specs/<슬러그>.py      다이어그램 한 장 = 파일 한 개 (30개)
  specs/_bootstrap.py   스펙이 도구를 가져오는 진입점
  lib/spec.py           스펙(N·E·Z) → SVG/HTML + Excalidraw
  lib/seq.py            시퀀스 전용 방출기 (생명선 · 활성 막대 · 자기 메시지)
  lib/ex.py             Excalidraw JSON 빌더
  lib/emit.py           출력 경로 결정 + emit() · emit_seq()
  lib/template.html     문서 머리말과 스타일 — 모든 그림이 여기서 온다
```

## 스펙 쓰는 법

좌표계는 SVG 픽셀이고, 원점은 왼쪽 위입니다. 같은 좌표가 Excalidraw 에도 그대로 쓰입니다.

```python
"""주문 도메인 클래스 — order-platform"""
from _bootstrap import N, E, Z, emit

nodes = [
 N(60, 120, 240, 134, 'storage', 'Customer', kind='class',
   attrs=['- id: Long'], ops=['+ placeOrder(): Order']),
]
edges = [E([(300, 187), (400, 187)], head=None)]

emit('order-platform', 'order-class', '주문 도메인 클래스', 1080, 700,
     '주문 도메인 클래스', '같은 도메인을 데이터가 아니라 책임과 관계로 본 그림',
     nodes, edges, zones, notes, labels, seed=101)
```

- `N(x, y, w, h, 색, 제목, [부제…])` — 색은 `input · process · storage · external · neutral · risk`
  여섯 가지 의미색만 씁니다. `kind` 로 `box`(기본) · `class` · `entity` · `diamond` · `ellipse`.
  제목을 `None` 으로 두면 글자 없는 상자가 됩니다 (겹쳐 그리는 그림자 등).
- `E([(x,y), …], 라벨, dashed=, head=, start=, lx=, ly=)` — `head`/`start` 는
  `arrow · open · tri · diamond · one · one-s · many · many-s`. 라벨 위치는 `lx`/`ly` 로 밀 수 있습니다.
- `Z(x, y, w, h, 라벨)` — 점선 영역(신뢰 경계 · 시스템 경계 · 레인).
- `labels` 는 정렬을 직접 지정해야 하는 글자용 `(x, y, 글자, 정렬)` 목록입니다.
- `notes` 는 그림 아래 각주로, 캔버스 바닥에서부터 자동으로 쌓입니다.
- `seed` 는 Excalidraw 의 손그림 흔들림을 고정합니다. **바꾸지 마세요** — 바꾸면 그림이 달라집니다.

시퀀스는 좌표계가 달라 `emit_seq(project, slug, …, actors, msgs, selfs, bars, notes)` 를 씁니다.
`specs/notify-sequence.py` 가 견본입니다.

**Excalidraw 규칙**: 글자가 들어가는 도형은 120×60 이상이어야 합니다 (스킬 규칙, `lib/ex.py` 가 강제).
작게 그리고 싶으면 도형에서 글자를 빼고 `labels` 로 따로 놓으세요.

## 그림을 고치는 순서

1. `specs/<슬러그>.py` 를 고친다
2. `python3 tools/generators/build.py <슬러그>` 로 다시 찍는다
3. 브라우저로 `diagram.html` 을 열어 눈으로 본다
4. 스펙과 산출물을 **함께** 커밋한다

새 그림이라면 `projects/<프로젝트>/diagrams/<슬러그>/meta.json` 도 만들고
`node tools/build-index.mjs` 로 목록을 갱신하세요.

## 알아둘 것

- 스펙은 **레이아웃을 계산해 주지 않습니다.** 좌표는 사람이 정합니다. 그래서 상자를 옮기면
  거기 붙은 선의 좌표도 같이 옮겨야 합니다.
- 글자 겹침은 자동으로 풀리지 않습니다. 촘촘한 그림은 찍은 뒤 눈으로 확인해야 합니다.
- Excalidraw 앱에서 손으로 고친 내용은 다음 생성 때 덮어씁니다. 편집은 스펙에서 하세요.
