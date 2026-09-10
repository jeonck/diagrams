"""알림 한 건의 지연 분해 (영문) — notify-hub-en"""
from _bootstrap import N, E, Z, emit

# 시간은 'Wait 2s' 처럼 짧게 써서 단계 이름이 원본 폭(200)에 그대로 들어간다 —
# 좌표는 원본 그대로 두고 캔버스 높이만 660 → 680 으로 늘려 주석 세 줄을 받았다.
# ── 값 흐름 ──
stages = [('Intake','20ms','—'),('Queue wait','—','1.5s'),('Worker run','80ms','—'),
          ('Provider handoff','300ms','—'),('Device arrival','—','2s')]
nodes, edges = [], []
for i,(name,pt,wt) in enumerate(stages):
    x = 60 + i*240
    nodes.append(N(x,170,200,110,'process',name,['Work '+pt,'Wait '+wt]))
    if i: edges.append(E([(x-40,225),(x,225)]))
nodes += [N(60,430,260,100,'storage','Total work time',['0.4s']),
          N(350,430,260,100,'risk','Total wait time',['3.5s']),
          N(640,430,260,100,'neutral','End-to-end latency',['3.9s']),
          N(930,430,260,100,'external','Flow efficiency',['0.4 ÷ 3.9 = 10%'])]
emit('notify-hub-en', 'notify-value-stream-en','Latency breakdown of one notification',1260,680,
 'Latency Breakdown of One Notification',
 'From intake to the screen: time spent working, time spent waiting', nodes, edges, (),
 ['Note: the numbers are illustrative. Replace them with real measurements.',
  'The value stream of the online shop is the lead time of one feature; this one is the real-time latency of one notification.',
  '90% of the latency is waiting, and most of that is arrival on the device — the part we can shorten is the 1.5s queue wait.'],
 (), 1209)
