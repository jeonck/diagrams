# 다이어그램 생성기 (있는 그대로 보관)

`projects/*/diagrams/*/diagram.html` 과 `diagram.excalidraw` 는 손으로 쓴 것이 아니라
여기 있는 스크립트가 스펙(노드·엣지 목록)에서 찍어낸 것입니다.

> **주의 — 아직 "원본"이 아닙니다.**
> 이 스크립트들은 작업할 때 쓰던 임시 배치 코드를 사라지기 전에 그대로 옮겨둔 것입니다.
> 지금은 **기록물**이지, 빌드에 물려 있는 파이프라인이 아닙니다.
> 아래 "알려진 문제"를 정리하고 CI 검증을 붙여야 비로소 원본이 됩니다.
> 그전까지 다이어그램을 고칠 때는 **산출물(diagram.html)과 여기 스펙을 함께** 고쳐야 합니다.

## 구성

**라이브러리** — 그리는 도구. 직접 실행하지 않습니다.

| 파일 | 하는 일 |
|---|---|
| `spec.py` | 스펙(`N` 노드 / `E` 엣지 / `Z` 영역) → SVG·HTML + Excalidraw. 화살표 마커, 클래스·엔터티 칸 구분선 포함 |
| `ex.py` | Excalidraw JSON 빌더 (`Doc`) — 도형·바인딩 텍스트·화살표 |
| `seq.py` | 시퀀스 다이어그램 전용 방출기 (생명선·활성 막대·자기 메시지) |
| `dg.py` | 초기 방출기. `spec.py` 의 전신 |

**배치 스크립트** — 실제로 그림을 찍는 쪽. 한 파일이 그림 2~4장을 담당합니다.

| 스크립트 | 만드는 다이어그램 |
|---|---|
| `b1.py` | order-class · package-deps · c4-container |
| `b2.py` | shop-usecase · order-state · checkout-activity |
| `b3.py` | order-dfd · fulfillment-bpmn · network-topology · value-stream |
| `ex3.py` | order-erd · deployment-topology · cicd-pipeline (**Excalidraw 만**) |
| `n1.py` | notify-usecase · notify-state · notify-c4 · notify-deployment |
| `n2.py` | notify-sequence |
| `n3.py` | notify-activity |
| `nA.py` | notify-class · notify-components · notify-packages |
| `nB.py` | notify-erd · notify-dfd · notify-network |
| `nC.py` | notify-bpmn · notify-cicd · notify-value-stream |

## 재현 확인 (2026-09-10 측정)

전부 다시 돌려 커밋본과 바이트 단위로 비교한 결과입니다.

| 형식 | 그대로 재현 | 생성기 없음 | 다르게 나옴 |
|---|---|---|---|
| `diagram.html` | 25 / 30 | 5 | **0** |
| `diagram.excalidraw` | 28 / 30 | 2 | **0** |

생성기가 있는 파일은 **하나도 빠짐없이 원본과 같습니다.**

생성기가 없는 그림 — 스펙 방식을 만들기 전에 그린 초기 그림들입니다.

- `mvc-structure` (html, excalidraw)
- `mvc-sequence` (html, excalidraw)
- `order-erd` (html)
- `deployment-topology` (html)
- `cicd-pipeline` (html)

## 지금 돌리는 법

경로가 `projects/` 재구조화 이전 기준이라, **저장소에서 그냥 돌리면 엉뚱한 곳에 씁니다.**
반드시 빈 미러 폴더에서 돌린 뒤 결과를 비교하세요.

```sh
# 1) 미러 폴더에 출력 자리를 만든다
rm -rf /tmp/regen && mkdir -p /tmp/regen
node -e "const j=require('./diagrams.json');for(const d of j.diagrams)console.log(d.project,d.id)" \
  | while read p s; do mkdir -p /tmp/regen/diagrams/$s /tmp/regen/projects/$p/diagrams/$s; done

# 2) 미러 폴더를 작업 폴더로 삼아 돌린다
cd /tmp/regen
for f in b1 b2 b3 ex3 n1 n2 n3 nA nB nC; do
  python3 /경로/tools/generators/$f.py
done

# 3) 커밋본과 비교한다 (다르면 스펙과 산출물이 어긋난 것)
diff /tmp/regen/diagrams/order-class/diagram.html \
     projects/order-platform/diagrams/order-class/diagram.html
```

`spec.py` · `seq.py` · `dg.py` 는 CSS 를 가져오려고
`/home/user/diagrams/projects/order-platform/diagrams/mvc-structure/diagram.html` 을
**절대 경로로 읽습니다.** 다른 곳에 두고 쓰려면 이 경로부터 고쳐야 합니다.

## 알려진 문제 (원본이 되기 전에 정리할 것)

1. **경로가 옛 구조** — 상대 경로 `diagrams/<슬러그>/` 를 씁니다. `projects/<프로젝트>/diagrams/<슬러그>/` 로 바꿔야 합니다.
2. **배치 묶음** — `b1.py`, `nA.py` 같은 이름에 그림 2~4장이 섞여 있어, 한 장을 고치려 할 때 어느 파일을 열지 알 수 없습니다. 슬러그별로 나눠야 합니다.
3. **순환 의존** — 생성기가 산출물(`mvc-structure/diagram.html`)을 CSS 원본으로 읽습니다. 템플릿을 별도 파일로 빼야 합니다.
4. **빠진 5장** — 위 목록의 그림들은 스펙을 새로 써야 합니다.
5. **CI 검증 없음** — 누군가 `diagram.html` 을 직접 고치면 스펙과 조용히 어긋납니다. `build-index.mjs --check` 처럼 "재생성본과 커밋본이 같은가" 를 배포 전에 확인해야 합니다.
