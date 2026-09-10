"""주문 기능 값 흐름 (영문) — order-platform-en"""
from _bootstrap import N, E, Z, emit

# ── Value stream ──
stages = [('Requirements','0.5d','2d'),('Design','1d','3d'),('Implementation','3d','1d'),
          ('Code Review','0.5d','4d'),('QA','1d','3d'),('Deploy','0.5d','2.5d')]
nodes, edges = [], []
for i,(name,pt,wt) in enumerate(stages):
    x = 60 + i*190
    nodes.append(N(x,180,170,110,'process',name,['Work '+pt,'Wait '+wt]))
    if i:
        edges.append(E([(x-20,235),(x,235)]))
nodes += [
 N(60,420,260,100,'storage','Total work time',['6.5 days']),
 N(350,420,260,100,'risk','Total wait time',['15.5 days']),
 N(640,420,260,100,'neutral','Lead time',['22 days']),
 N(930,420,260,100,'external','Flow efficiency',['6.5 ÷ 22 = 30%']),
]
emit('order-platform-en', 'value-stream-en','Order feature value stream',1250,640,'Order Feature Value Stream',
     'From one request to a deployment: time spent working, time spent waiting', nodes, edges, (),
     ['Note: The numbers are illustrative. Replace them with your own measurements.',
      '70% of the lead time is waiting — cutting the waiting pays off far more than speeding up each stage.'],
     [], seed=804)
