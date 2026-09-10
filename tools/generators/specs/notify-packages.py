"""모듈 의존 구조 — notify-hub"""
from _bootstrap import N, E, Z, emit

# ── 패키지 ──
emit('notify-hub', 'notify-packages','모듈 의존 구조',1080,660,'모듈 의존 구조',
 '따로 배포되는 두 모듈이 하나의 도메인을 공유하는 방식',
 [N(320,120,300,90,'input','notify-api',['배포 단위 · 수신']),
  N(700,120,300,90,'input','notify-worker',['배포 단위 · 발송']),
  N(510,300,300,90,'storage','notify-core',['도메인 · 포트']),
  N(510,460,300,90,'neutral','notify-adapters',['SQS · 공급자 · DB'])],
 [E([(470,210),(600,300)],'«use»',dashed=True,head='open',lx=470,ly=270),
  E([(850,210),(760,300)],'«use»',dashed=True,head='open',lx=880,ly=270),
  E([(660,460),(660,390)],'«use»',dashed=True,head='open',lx=730,ly=430)],
 (),
 ['※ notify-api 와 notify-worker 는 따로 배포되지만 같은 도메인 모듈을 씁니다.',
  'notify-core 에서 나가는 화살표가 없다는 점은 온라인 상점의 domain 과 같은 규칙입니다.'],
 [(400,350,'나가는 의존 없음',None)], 703)
