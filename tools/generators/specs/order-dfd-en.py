"""Order data flow (level 1) — order-platform-en"""
from _bootstrap import N, E, Z, emit

# ── DFD ──
# 영문 처리 이름이 길어 타원 폭을 230 → 270 으로 넓히고 x 를 340 으로 당겼다
# (중심선 x=475 는 원본 그대로라 세로 흐름은 같은 자리에 남는다).
nodes = [
 N(60,180,170,90,'external','Customer'),
 N(340,160,270,110,'process','1.0 Receive order',kind='ellipse'),
 N(340,390,270,110,'process','2.0 Process payment',kind='ellipse'),
 N(340,620,270,110,'process','3.0 Prepare shipping',kind='ellipse'),
 N(720,175,240,80,'storage','D1 Order store'),
 N(720,400,240,90,'neutral','Payment Gateway'),
 N(720,625,240,80,'storage','D2 Inventory store'),
]
edges = [
 E([(230,215),(340,215)], 'Order details', ly=198),
 E([(610,205),(720,205)], 'Order record', ly=188),
 E([(475,270),(475,390)], 'Payable order', lx=545, ly=334),
 E([(610,425),(720,425)], 'Auth request', ly=408),
 E([(720,470),(610,470)], 'Auth result', ly=490),
 E([(475,500),(475,620)], 'Payment done', lx=545, ly=564),
 E([(610,665),(720,665)], 'Stock drawdown', lx=657, ly=648),
 E([(340,690),(150,690),(150,270)], 'Shipping notice', lx=250, ly=674),
]
emit('order-platform-en', 'order-dfd-en','Order Data Flow (Level 1)',1080,820,'Order Data Flow (Level 1)',
     'Which processes order data passes through, and where it comes to rest', nodes, edges, (),
     ['Note: an ellipse is a process, a rectangle named D-something is a data store, and any other rectangle is an external entity.',
      'A DFD draws the movement of data only, never control flow — it says nothing about ordering or branching.'],
     [], seed=801)
