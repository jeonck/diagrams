"""Order domain classes — order-platform-en"""
from _bootstrap import N, E, Z, emit

# ── classes ──
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
          (912,350,'inherits',None)]
emit('order-platform-en', 'order-class-en','Order Domain Classes',1080,700,'Order Domain Classes',
     'The same domain seen through responsibilities and relationships, not data', nodes, edges, (),
     ['Note: The filled diamond is composition — when an Order goes away, its Order Items go with it.',
      'The hollow triangle is inheritance, and the numbers are multiplicity. Unlike an ERD, the operations (behaviour) show up too.'],
     labels, seed=601)
