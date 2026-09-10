"""패키지 의존 구조 — order-platform"""
from _bootstrap import N, E, Z, emit

# ── 패키지 ──
nodes = [
 N(380,130,300,90,'input','web',['컨트롤러 · 뷰 · DTO']),
 N(380,290,300,90,'process','application',['유스케이스 · 트랜잭션 경계']),
 N(380,450,300,90,'storage','domain',['엔티티 · 값 객체 · 포트']),
 N(760,290,280,90,'neutral','infrastructure',['JPA · 외부 API 어댑터']),
]
edges = [
 E([(530,220),(530,290)], '«use»', dashed=True, head='open', lx=575, ly=260),
 E([(530,380),(530,450)], '«use»', dashed=True, head='open', lx=575, ly=420),
 E([(880,380),(690,470)], '«use»', dashed=True, head='open', lx=768, ly=398),
]
emit('order-platform', 'package-deps','패키지 의존 구조',1080,660,'패키지 의존 구조',
     '어느 패키지가 어느 패키지를 알아도 되는가', nodes, edges, (),
     ['※ 화살표는 “이 패키지가 저 패키지를 안다”는 뜻입니다.',
      'domain 에서 나가는 화살표가 하나도 없다는 점이 핵심입니다 — 도메인은 아무것도 의존하지 않습니다.'],
     [(700,505,'나가는 의존 없음',None)], seed=102)
