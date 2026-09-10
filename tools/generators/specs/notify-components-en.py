"""Intake API components — notify-hub-en"""
from _bootstrap import N, E, Z, emit

# ── components ──
# 부제가 영어로 길어졌지만 상자 폭(380 · 200)에 들어가 좌표는 원본 그대로 두었다.
emit('notify-hub-en', 'notify-components-en','Intake API Components',1080,700,'Intake API Components',
 'The parts a single request passes through inside the Intake API',
 [N(350,150,380,70,'input','HTTP Controller',['Validates request · responds']),
  N(350,250,380,70,'process','Idempotency Filter',['Filters duplicates by idempotency key']),
  N(350,350,380,70,'process','Notification Service',['Intake processing flow']),
  N(330,460,200,70,'storage','History Repository'),
  N(560,460,200,70,'storage','Queue Publisher'),
  N(60,455,200,80,'neutral','History DB'),
  N(850,455,200,80,'neutral','Event Queue')],
 [E([(540,220),(540,250)]),
  E([(540,320),(540,350)]),
  E([(430,420),(430,460)]),
  E([(660,420),(660,460)]),
  E([(330,495),(260,495)]),
  E([(760,495),(850,495)])],
 [Z(300,110,480,470,'Intake API')],
 ['Note: the boxes inside the dashed border are the components; the two outside are external resources they use.',
  'The idempotency filter sitting right after the controller is point ② of ADR 0003.'],
 (), 1202)
