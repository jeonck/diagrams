"""Notification send state transitions — notify-hub-en"""
from _bootstrap import N, E, Z, emit

# ── state machine ──
# 영문 상태 이름이 길어 "Given up (DLQ)" 상자만 170 → 190 으로 넓히고
# x 를 740 → 730 으로 당겨 중심선(x=825)을 원본 그대로 두었다.
# 상자 사이 간격(80px)에 들어가도록 전이 라벨은 짧은 단어를 골랐고,
# 대각선 라벨은 lx 를 520 → 560 으로 밀어 선에 붙였다.
emit('notify-hub-en', 'notify-state-en','Notification Send State Transitions',1220,760,
 'Notification Send State Transitions',
 'One notification from intake until it either succeeds or is given up',
 [N(60,190,120,60,'neutral','Start'),
  N(240,180,170,80,'input','Accepted'),
  N(490,180,170,80,'process','Queued'),
  N(740,180,170,80,'process','Sending'),
  N(990,180,170,80,'storage','Sent'),
  N(740,370,170,80,'risk','Failed'),
  N(490,370,170,80,'process','Retry wait'),
  N(730,550,190,80,'risk','Given up (DLQ)'),
  N(990,555,120,60,'neutral','End')],
 [E([(180,220),(240,220)]),
  E([(410,220),(490,220)],'Enqueued',ly=202),
  E([(660,220),(740,220)],'Claimed',ly=202),
  E([(910,220),(990,220)],'Send OK',ly=202),
  E([(825,260),(825,370)],'Error · timeout',lx=920,ly=320),
  E([(740,410),(660,410)],'< 5 tries',ly=392),
  E([(575,370),(775,260)],'Retry after backoff',lx=560,ly=305),
  E([(825,450),(825,550)],'> 5 tries',lx=890,ly=505),
  E([(1075,260),(1170,260),(1170,585),(1110,585)]),
  E([(920,590),(990,590)])],
 (),
 ['Note: retries use exponential backoff up to 5 times; after that the notification goes to the DLQ and is given up.',
  '“Given up” is an end state too — nothing vanishes quietly, every case stays on the record.'],
 (), 902)
