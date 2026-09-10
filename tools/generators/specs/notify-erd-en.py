"""Notification domain ERD — notify-hub-en"""
from _bootstrap import N, E, Z, emit

# ── ERD ──
# 테이블·컬럼 이름은 원본이 이미 영문이라 좌표를 그대로 두었고,
# 관계 라벨만 영어로 옮기면서 겹치지 않게 lx/ly 를 조금 밀었다.
emit('notify-hub-en', 'notify-erd-en','Notification Domain ERD',1080,720,'Notification Domain ERD',
 'The tables that hold recipients, notifications and delivery attempts',
 [N(60,110,220,110,'storage','recipient',kind='entity',attrs=['PK  recipient_id','user_id','locale']),
  N(400,110,260,130,'process','notification',kind='entity',attrs=['PK  notification_id','FK  recipient_id','idempotency_key  UNIQUE','status']),
  N(60,390,220,110,'process','channel_preference',kind='entity',attrs=['PK  pref_id','FK  recipient_id','channel · enabled']),
  N(400,390,260,130,'process','delivery_attempt',kind='entity',attrs=['PK  attempt_id','FK  notification_id','attempt_no','result'])],
 [E([(280,173),(400,173)],head='many',start='one-s'),
  E([(170,220),(170,390)],head='many',start='one-s'),
  E([(530,240),(530,390)],head='many',start='one-s')],
 (),
 ['Note: the crow’s foot marks the N side and the short bar the 1 side.',
  'idempotency_key is enforced by a unique constraint on notification, with no separate store (ADR 0003).'],
 [(340,146,'N per recipient','middle'),(190,310,'Channel preference',None),(550,320,'Delivery attempt',None)], 1204)
