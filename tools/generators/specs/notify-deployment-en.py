"""알림 허브 배포 구성 (영문) — notify-hub-en"""
from _bootstrap import N, E, Z, emit

# 영어 라벨이 길어 DLQ · 이력 DB 열을 660 → 680 으로 밀어 'Record result' 가 들어갈
# 폭을 만들고, 외부 공급자 상자를 200 → 220 으로 넓혔다. 배치 자체는 원본과 같다.
# ── 배포 구성 ──
emit('notify-hub-en', 'notify-deployment-en','Notification Hub deployment',1200,800,'Notification Hub Deployment',
 'Intake and sending scale separately, with the queue between them',
 [N(60,230,200,90,'external','Sending Service'),
  N(340,200,240,90,'process','Intake API ×2',['Stateless']),
  N(340,370,240,80,'storage','Event Queue'),
  N(340,540,240,90,'process','Send Workers ×4',['Scales with queue depth']),
  N(680,370,220,80,'risk','DLQ'),
  N(680,540,220,90,'storage','Delivery History DB'),
  N(960,540,220,90,'neutral','External Providers')],
 [E([(260,275),(340,245)],'Request',lx=300,ly=242),
  E([(460,290),(460,370)],'Enqueue',lx=515,ly=334),
  E([(460,450),(460,540)],'Claim',lx=510,ly=498),
  E([(580,410),(680,410)],'After 5 tries',ly=392,dashed=True),
  E([(580,585),(680,585)],'Record result',ly=568),
  E([(900,585),(960,585)],'Send',ly=568)],
 [Z(300,150,620,540,'Private subnet')],
 ['Note: the intake API and the send workers scale separately across the queue — when traffic spikes,',
  'intake only has to enqueue, and the backlog is worked off by adding more workers.'],
 (), 904)
