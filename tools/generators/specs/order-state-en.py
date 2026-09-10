"""Order state transitions — order-platform-en"""
from _bootstrap import N, E, Z, emit

# ── state machine ──
# 영문 상태 이름이 한국어보다 길어 가로 간격을 넓혔다 (원본 대비 x 재배치).
nodes = [
 N(40,180,120,60,'neutral','Start'),
 N(230,170,190,80,'input','Placed'),
 N(560,170,190,80,'process','Paid'),
 N(890,170,190,80,'process','Preparing'),
 N(890,360,190,80,'process','Shipping'),
 N(560,360,190,80,'storage','Delivered'),
 N(230,360,190,80,'risk','Cancelled'),
 N(595,560,120,60,'neutral','End'),
]
edges = [
 E([(160,210),(230,210)]),
 E([(420,210),(560,210)], 'Payment approved', ly=192),
 E([(750,210),(890,210)], 'Stock reserved', ly=192),
 E([(985,250),(985,360)], 'Dispatched', lx=1045, ly=310),
 E([(890,400),(750,400)], 'Receipt confirmed', lx=820, ly=378),
 E([(325,250),(325,360)], 'Customer cancels', lx=235, ly=310),
 E([(620,250),(390,360)], 'Payment cancelled · refunded', lx=700, ly=320),
 E([(655,440),(655,560)]),
 E([(325,440),(325,590),(595,590)]),
]
emit('order-platform-en', 'order-state-en','Order State Transitions',1200,720,'Order State Transitions',
     'The states a single order can be in, and the events that change them',
     nodes, edges, (),
     ['Note: a box is a state; the words on an arrow are the event that causes that transition.',
      '“Start” and “End” stand in for the UML initial and final pseudostates. Only Delivered and Cancelled are end states.'],
     [], seed=701)
