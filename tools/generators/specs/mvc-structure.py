"""MVC 구조 — order-platform"""
from _bootstrap import N, E, Z, emit

nodes = [
 N(340,98,220,84,'input','사용자 (User)',['브라우저 · 클라이언트']),
 N(70,306,240,104,'process','Controller',['입력 해석 · 흐름 제어','요청 라우팅 · 유효성 검증']),
 N(590,306,240,104,'external','View',['표현 · 렌더링','템플릿 · 화면 구성']),
 N(330,522,240,104,'storage','Model',['도메인 데이터 · 상태','비즈니스 규칙 · 영속성']),
]
edges = [
 E([(390,182),(190,306)]),
 E([(710,306),(510,182)]),
 E([(190,410),(390,522)]),
 E([(510,522),(710,410)]),
 E([(310,358),(590,358)], dashed=True),
]
# 화살표 글자는 선을 피해 바깥쪽에 붙인다 — 정렬이 제각각이라 labels 로 둔다
labels = [
 (250,246,'① 사용자 입력 · 요청','end'),
 (650,246,'④ 화면 응답',None),
 (270,490,'② 상태 변경 요청','end'),
 (630,490,'③ 변경 통지 · 데이터 조회',None),
 (450,348,'뷰 선택 · 갱신 지시','middle'),
]
emit('order-platform', 'mvc-structure', 'MVC 다이어그램', 900, 710,
     'MVC (Model–View–Controller) 패턴',
     '사용자 입력 → 제어 → 상태 변경 → 화면 갱신으로 이어지는 순환 구조',
     nodes, edges, (),
     ['※ 점선은 변형에 따라 달라지는 경로입니다. Observer 변형에서는 Model이 View에',
      '직접 변경을 통지하고, Passive View 변형에서는 Controller가 View를 갱신합니다.'],
     labels, seed=1)
