"""알림 허브 유스케이스 (영문) — notify-hub-en"""
from _bootstrap import N, E, Z, emit

# ── 유스케이스 ──
# 영어 유스케이스 문구가 길어 타원 폭을 240 → 280 으로 넓히고 x 를 350 → 340 으로 당겼다.
# (경계 상자 안에 그대로 들어가고, 배치 뼈대는 원본과 같다.)
emit('notify-hub-en', 'notify-usecase-en','Notification Hub Use Cases',1160,780,'Notification Hub Use Cases',
 'Who does what with this service',
 [N(60,200,190,90,'external','Sending service',['e.g. order platform']),
  N(60,430,190,90,'external','User'),
  N(910,400,190,90,'external','Operator'),
  N(340,180,280,90,'input','Send a notification',kind='ellipse'),
  N(340,310,280,90,'process','Manage channel preferences',kind='ellipse'),
  N(340,440,280,90,'process','View delivery history',kind='ellipse'),
  N(340,540,280,90,'process','Resend failed notifications',kind='ellipse')],
 [E([(250,245),(340,225)], head=None),
  E([(250,465),(340,355)], head=None),
  E([(250,480),(340,485)], head=None),
  E([(910,425),(620,485)], head=None),
  E([(910,450),(620,585)], head=None)],
 [Z(300,130,560,520,'Notification Hub (system boundary)')],
 ['Note: the sending service is not a person, but it pushes requests in from outside, so it is drawn as an actor.',
  'Receiving a notification is not a use case — only the things a user asks the system to do are use cases.'],
 (), 901)
