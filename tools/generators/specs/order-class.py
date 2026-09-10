"""주문 도메인 클래스 — order-platform"""
from _bootstrap import N, E, Z, emit

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
emit('order-platform', 'order-class','주문 도메인 클래스',1080,700,'주문 도메인 클래스',
     '같은 도메인을 데이터가 아니라 책임과 관계로 본 그림', nodes, edges, (),
     ['※ 속이 찬 마름모는 합성입니다 — 주문이 사라지면 주문항목도 함께 사라집니다.',
      '빈 삼각형은 상속이고, 숫자는 다중도입니다. ERD 와 달리 오퍼레이션(행동)이 함께 드러납니다.'],
     labels, seed=101)
