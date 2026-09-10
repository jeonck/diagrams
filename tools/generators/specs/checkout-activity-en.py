"""Checkout activity — order-platform-en"""
from _bootstrap import N, E, Z, emit

# ── activities ──
nodes = [
 N(400,110,120,60,'neutral','Start'),
 N(370,220,220,80,'process','Check cart'),
 N(360,350,240,110,'external','In stock?',kind='diamond'),
 N(50,375,240,80,'risk','Notify sold out'),
 N(370,510,220,80,'process','Request payment'),
 N(330,640,300,10,'neutral',None),
 N(150,700,220,80,'process','Confirm order'),
 N(590,700,220,80,'process','Deduct inventory'),
 N(330,830,300,10,'neutral',None),
 N(350,880,260,80,'process','Send confirmation email'),
 N(400,1010,120,60,'neutral','End'),
]
edges = [
 E([(460,170),(460,220)]),
 E([(480,300),(480,350)]),
 E([(360,405),(290,405)], '[No]', lx=325, ly=390),
 E([(480,460),(480,510)], '[Yes]', lx=520, ly=490),
 E([(480,590),(480,640)]),
 E([(400,650),(260,700)]),
 E([(560,650),(700,700)]),
 E([(260,780),(400,830)]),
 E([(700,780),(560,830)]),
 E([(480,840),(480,880)]),
 E([(480,960),(480,1010)]),
 E([(170,455),(170,1040),(400,1040)]),
]
emit('order-platform-en', 'checkout-activity-en','Checkout Activity',1000,1180,'Checkout Activity',
     'From cart to confirmation email — a flow with a branch and a parallel split',
     nodes, edges, (),
     ['Note: the diamond is a decision, and the thick bars are the fork and join of the parallel part.',
      'Confirm order and Deduct inventory have no set order; both must finish before the flow moves on.'],
     [(650,648,'fork',None),(650,838,'join',None)], seed=702)
