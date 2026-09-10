"""주문 이행 프로세스 (BPMN, 영문) — order-platform-en"""
from _bootstrap import N, E, Z, emit

# ── BPMN ──
# 영어 라벨이 길어 시작 이벤트 타원과 취소 상자 폭을 넓히고, 그에 맞춰 연결선 시작점을 옮겼다.
zones = [Z(150,150,1010,250,'Store — Order handling'), Z(150,440,1010,230,'Store — Shipping')]
nodes = [
 N(180,205,150,100,'neutral','Order placed',kind='ellipse'),
 N(360,215,200,90,'process','Verify payment'),
 N(610,195,210,130,'external','Payment OK?',kind='diamond'),
 N(880,215,200,90,'risk','Send cancel notice'),
 N(360,490,200,90,'process','Pack items'),
 N(620,490,200,90,'process','Hand to carrier'),
 N(890,490,130,90,'neutral','Done',kind='ellipse'),
]
edges = [
 E([(330,255),(360,260)]),
 E([(560,260),(610,260)]),
 E([(820,260),(880,260)], 'No', ly=242),
 E([(715,325),(715,420),(460,420),(460,490)], 'Yes', lx=742, ly=370),
 E([(560,535),(620,535)]),
 E([(820,535),(890,535)]),
 E([(1080,305),(1120,305),(1120,535),(1020,535)]),
]
emit('order-platform-en', 'fulfillment-bpmn-en','Order Fulfillment Process (BPMN)',1200,760,
     'Order Fulfillment Process (BPMN)',
     'How a single order moves from team to team', nodes, edges, zones,
     ['Note: the horizontal bands are lanes (who does the work), circles are start and end events, and diamonds are gateways (branches).',
      'An arrow that crosses a lane is a handover, and handovers are where BPMN processes most often go wrong.'],
     [], seed=803)
