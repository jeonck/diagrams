import sys; sys.path.insert(0, '/tmp/dg')
from spec import N, E, Z, emit_svg, emit_ex

def both(slug, doc, w, h, title, sub, nodes, edges, zones=(), notes=(), labels=(), seed=1):
    emit_svg('diagrams/%s/diagram.html' % slug, doc, w, h, title, sub, nodes, edges, zones, notes, labels)
    n = emit_ex('diagrams/%s/diagram.excalidraw' % slug, title, sub, nodes, edges, zones, notes, labels, seed)
    print(slug, '->', n, 'excalidraw elements')

# ── 클래스 ──
nodes = [
 N(60,120,240,134,'storage','Customer',kind='class',attrs=['- id: Long','- email: String'],ops=['+ placeOrder(): Order']),
 N(400,120,280,174,'process','Order',kind='class',attrs=['- id: Long','- placedAt: Instant','- status: OrderStatus'],ops=['+ total(): Money','+ cancel(): void']),
 N(780,120,240,132,'process','Payment',kind='class',stereo='«abstract»',attrs=['- amount: Money'],ops=['+ approve(): boolean']),
 N(60,440,240,134,'storage','Product',kind='class',attrs=['- name: String','- price: Money'],ops=['+ isAvailable(): boolean']),
 N(400,440,280,114,'process','OrderItem',kind='class',attrs=['- quantity: int'],ops=['+ subtotal(): Money']),
 N(780,440,240,114,'process','CardPayment',kind='class',attrs=['- maskedNo: String'],ops=['+ approve(): boolean']),
]
edges = [
 E([(300,187),(400,187)], head=None),
 E([(540,294),(540,440)], head=None, start='diamond'),
 E([(400,507),(300,507)], head=None),
 E([(680,187),(780,187)], head=None),
 E([(900,440),(900,252)], head='tri'),
]
labels = [(310,180,'1',None),(392,180,'0..*','end'),(552,318,'1',None),(552,432,'1..*',None),
          (392,500,'0..*','end'),(310,500,'1',None),(690,180,'1',None),(772,180,'1','end'),
          (912,350,'상속',None)]
both('order-class','주문 도메인 클래스',1080,700,'주문 도메인 클래스',
     '같은 도메인을 데이터가 아니라 책임과 관계로 본 그림', nodes, edges, (),
     ['※ 속이 찬 마름모는 합성입니다 — 주문이 사라지면 주문항목도 함께 사라집니다.',
      '빈 삼각형은 상속이고, 숫자는 다중도입니다. ERD 와 달리 오퍼레이션(행동)이 함께 드러납니다.'],
     labels, seed=101)

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
both('package-deps','패키지 의존 구조',1080,660,'패키지 의존 구조',
     '어느 패키지가 어느 패키지를 알아도 되는가', nodes, edges, (),
     ['※ 화살표는 “이 패키지가 저 패키지를 안다”는 뜻입니다.',
      'domain 에서 나가는 화살표가 하나도 없다는 점이 핵심입니다 — 도메인은 아무것도 의존하지 않습니다.'],
     [(700,505,'나가는 의존 없음',None)], seed=102)

# ── C4 컨테이너 ──
zones = [Z(340,150,580,400,'온라인 상점 — 우리가 만드는 시스템')]
nodes = [
 N(60,190,220,100,'external','고객',['[Person]','주문하는 사람']),
 N(390,190,240,100,'input','웹 앱',['[Container: SPA]']),
 N(390,370,240,110,'process','API 애플리케이션',['[Container: Spring]']),
 N(690,370,210,110,'storage','데이터베이스',['[Container: PostgreSQL]']),
 N(340,650,250,100,'neutral','결제 게이트웨이',['[External System]']),
 N(650,650,250,100,'neutral','이메일 시스템',['[External System]']),
]
edges = [
 E([(280,240),(390,240)], '주문', ly=224),
 E([(510,290),(510,370)], '[JSON/HTTPS]', lx=580, ly=334),
 E([(630,425),(690,425)], None),
 E([(460,480),(460,650)], '결제 승인 [HTTPS]', lx=350, ly=570),
 E([(570,480),(760,650)], '주문 확인 [SMTP]', lx=830, ly=600),
]
both('c4-container','C4 컨텍스트·컨테이너',1120,830,'C4 컨텍스트·컨테이너',
     '시스템 경계 안의 컨테이너와, 경계 밖의 사람·외부 시스템', nodes, edges, zones,
     ['※ C4 의 컨테이너(2단계) 수준입니다. 점선 안은 우리가 배포하는 것, 밖은 우리가 만들지 않는 것입니다.',
      '컨테이너는 도커 컨테이너가 아니라 “따로 배포되고 따로 돌아가는 단위”를 뜻합니다.'],
     [(660,406,'읽기·쓰기',None)], seed=103)
