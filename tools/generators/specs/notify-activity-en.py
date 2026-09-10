"""Notification send retry activity — notify-hub-en"""
from _bootstrap import N, E, Z, emit

# ── activities ──
# 흐름의 뼈대(중심선 x=540)는 원본 그대로다. 영어 문구가 길어진 상자 셋만 폭을
# 240·260 → 280 으로 넓히고 x 를 420·400 → 400 으로 당겨 중심을 540 에 그대로 두었다.
# 마름모(260x120)는 넓히지 않고 질문을 짧게 잡았다 — 'Claim succeeded?',
# 'Under 5 retries?' 는 마름모 가운데 폭 안에 들어간다.
# 분기 라벨은 길어진 만큼 lx 를 조금씩 밀어 상자·마름모와 띄웠다 (358→366, 612→616).
nodes = [
 N(480,70,120,60,'neutral','Start'),
 N(400,170,280,80,'process','Receive message from queue'),
 N(410,290,260,120,'external','Claim succeeded?',kind='diamond'),
 N(60,310,240,80,'neutral','Duplicate — skip quietly'),
 N(400,470,280,80,'process','Send request to provider'),
 N(410,590,260,120,'external','Succeeded?',kind='diamond'),
 N(760,610,240,80,'storage','Record history · ack'),
 N(410,770,260,120,'external','Under 5 retries?',kind='diamond'),
 N(110,790,220,80,'process','Backoff wait',['1 · 2 · 4 · 8 · 16s']),
 N(400,960,280,80,'risk','Move to DLQ · mark given up'),
 N(480,1080,120,60,'neutral','End'),
]
edges = [
 E([(540,130),(540,170)]),
 E([(540,250),(540,290)]),
 E([(410,350),(300,350)],'[0 rows updated]',lx=366,ly=332),
 E([(540,410),(540,470)],'[1 row updated]',lx=616,ly=446),
 E([(60,350),(30,350),(30,1110),(480,1110)]),
 E([(540,550),(540,590)]),
 E([(670,650),(760,650)],'[Success]',ly=632),
 E([(880,690),(880,1110),(600,1110)]),
 E([(540,710),(540,770)],'[Failure]',lx=600,ly=746),
 E([(410,830),(330,830)],'[Under 5]',ly=812),
 E([(220,790),(220,510),(400,510)],'Retry after backoff',lx=300,ly=650),
 E([(540,890),(540,960)],'[5 or more]',lx=608,ly=930),
 E([(540,1040),(540,1080)]),
]
notes = ['Note: a diamond is a branch. The first branch is the worker-stage guard from ADR 0003 —',
 'a conditional UPDATE claims the row, so even when the queue hands over the same message twice only one worker sends it.',
 'A retry is drawn as another trip around the same cycle.']

emit('notify-hub-en', 'notify-activity-en', 'Notification Send Retry Activity', 1080, 1290,
     'Notification Send Retry Activity',
     'One send-worker cycle — claim, then succeed, loop after backoff, or give up',
     nodes, edges, (), notes, (), seed=1101)
