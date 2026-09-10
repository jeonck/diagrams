"""쇼핑몰 유스케이스 (영문) — order-platform-en"""
from _bootstrap import N, E, Z, emit

# ── 유스케이스 ──
# 영어 라벨이 길어 타원/상자 폭을 원본보다 조금 넓혔다 (배치 뼈대는 원본 그대로).
zones = [Z(300,120,540,560,'Online Store (system boundary)')]
nodes = [
 N(60,290,160,90,'external','Customer'),
 N(920,180,160,90,'external','Admin'),
 N(890,540,210,90,'neutral','Payment Gateway'),
 N(350,160,240,90,'input','Search products',kind='ellipse'),
 N(350,290,240,90,'input','Add to cart',kind='ellipse'),
 N(350,420,240,90,'process','Place an order',kind='ellipse'),
 N(350,550,240,90,'process','Pay',kind='ellipse'),
 N(610,160,210,90,'storage','Manage inventory',kind='ellipse'),
]
edges = [
 E([(220,320),(350,210)], head=None),
 E([(220,330),(350,330)], head=None),
 E([(220,345),(350,460)], head=None),
 E([(220,360),(350,590)], head=None),
 E([(920,230),(820,205)], head=None),
 E([(590,595),(890,585)], head=None),
]
emit('order-platform-en', 'shop-usecase-en','Online Store Use Cases',1120,780,'Online Store Use Cases',
     'Who can do what with this system',
     nodes, edges, zones,
     ['Note: ellipses are use cases and the outer boxes are actors. Everything inside the dashed line is the system we are building.',
      'The payment gateway is a system rather than a person, but it takes part from outside the boundary, so it is drawn as an actor.'],
     [], seed=703)
