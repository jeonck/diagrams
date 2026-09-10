"""알림 허브 네트워크 토폴로지 (영문) — notify-hub-en"""
from _bootstrap import N, E, Z, emit

# 왼쪽 두 상자는 영어 이름이 길어 220 → 240 으로 넓혔고(x 는 그대로 60),
# 선 시작점을 280 → 300 으로 따라 옮겼다. '443 outbound' 는 원본처럼 세로선
# 오른쪽에 두면 선과 VPC 경계를 함께 넘어서, 선 왼쪽의 빈 자리로 옮겼다.
# 주석 세 줄이 길어져 VPC 점선에 닿기에 캔버스 높이만 900 → 940 으로 늘렸다.
# ── 네트워크 토폴로지 ──
emit('notify-hub-en', 'notify-network-en','Notification Hub network topology',1180,940,'Notification Hub Network Topology',
 'What sits in which subnet, and where traffic leaves',
 [N(60,265,240,90,'external','Internal Services'),
  N(420,270,220,80,'process','Intake API ×2'),
  N(760,270,240,80,'process','Send Workers ×4'),
  N(420,470,220,90,'storage','Delivery History DB'),
  N(760,470,240,90,'neutral','SQS VPC Endpoint'),
  N(760,680,240,80,'process','NAT Gateway'),
  N(60,680,240,90,'external','Push · Email Providers')],
 [E([(300,310),(420,310)],'443',ly=292),
  E([(530,350),(530,470)],'5432',lx=585,ly=414),
  E([(640,330),(700,330),(700,515),(760,515)],'Enqueue',lx=674,ly=320),
  E([(880,470),(880,350)],'Claim',lx=932,ly=414),
  E([(1000,310),(1080,310),(1080,720),(1000,720)],'443 outbound',lx=1020,ly=635),
  E([(760,720),(300,720)],'Internet',ly=703)],
 [Z(320,180,820,640,'VPC 10.20.0.0/16'),
  Z(360,240,740,150,'Private subnet · App 10.20.10.0/24'),
  Z(360,440,740,160,'Private subnet · Data 10.20.20.0/24'),
  Z(360,650,740,130,'Public subnet 10.20.1.0/24')],
 ['Note: nothing reaches this service from the internet — requests only come from the internal service network.',
  'Only outbound traffic passes through NAT to reach the providers. The queue is attached over a VPC endpoint, so it never crosses the internet.',
  'The send workers also talk to the history DB over 5432 — the lines would overlap, so only the intake API path is drawn.'],
 (), 1206)
