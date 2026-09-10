"""Notification data flow (level 1) — notify-hub-en"""
from _bootstrap import N, E, Z, emit

# ── DFD ──
# 영문 처리·저장소 이름이 길어 타원 폭을 230 → 250, 저장소 폭을 240 → 260 으로
# 넓혔다. 타원 x(340)는 원본 그대로라 세로 흐름은 같은 자리에 남고,
# 타원 중심선만 455 → 465 로 밀려 세로 연결선과 그 라벨을 함께 옮겼다.
# 가로 라벨(Message payload 등)이 들어갈 틈을 벌리려 오른쪽 열 x 를 700 → 720 으로 밀었다.
emit('notify-hub-en', 'notify-dfd-en','Notification Data Flow (Level 1)',1080,840,
 'Notification Data Flow (Level 1)',
 'Which processes notification data passes through, and where it comes to rest',
 [N(60,180,180,90,'external','Sending service'),
  N(340,170,250,110,'process','1.0 Intake',kind='ellipse'),
  N(720,185,260,80,'storage','D1 Notification store'),
  N(340,400,250,110,'process','2.0 Send',kind='ellipse'),
  N(720,410,260,90,'neutral','External provider'),
  N(340,630,250,110,'process','3.0 Retry · give up',kind='ellipse'),
  N(720,635,260,80,'storage','D2 Delivery history')],
 [E([(240,225),(340,225)],'Send request',ly=208),
  E([(590,215),(720,215)],'Intake record',ly=198),
  E([(465,280),(465,400)],'Due to send',lx=535,ly=344),
  E([(590,440),(720,440)],'Message payload',ly=423),
  E([(720,470),(590,470)],'Send result',ly=490),
  E([(465,510),(465,630)],'Failed items',lx=535,ly=574),
  E([(590,675),(720,675)],'Delivery attempt',ly=658)],
 (),
 ['Note: an ellipse is a process, a rectangle named D-something is a data store, and the rest are external entities.',
  'A DFD draws the movement of data only — control such as how many times a retry runs lives in the state transition diagram.'],
 (), 1205)
