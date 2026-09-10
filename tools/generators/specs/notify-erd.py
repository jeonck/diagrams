"""알림 도메인 ERD — notify-hub"""
from _bootstrap import N, E, Z, emit

# ── ERD ──
emit('notify-hub', 'notify-erd','알림 도메인 ERD',1080,720,'알림 도메인 ERD',
 '수신자와 알림, 그리고 시도 기록이 놓이는 표',
 [N(60,110,220,110,'storage','recipient',kind='entity',attrs=['PK  recipient_id','user_id','locale']),
  N(400,110,260,130,'process','notification',kind='entity',attrs=['PK  notification_id','FK  recipient_id','idempotency_key  UNIQUE','status']),
  N(60,390,220,110,'process','channel_preference',kind='entity',attrs=['PK  pref_id','FK  recipient_id','channel · enabled']),
  N(400,390,260,130,'process','delivery_attempt',kind='entity',attrs=['PK  attempt_id','FK  notification_id','attempt_no','result'])],
 [E([(280,173),(400,173)],head='many',start='one-s'),
  E([(170,220),(170,390)],head='many',start='one-s'),
  E([(530,240),(530,390)],head='many',start='one-s')],
 (),
 ['※ 까마귀발이 N 쪽, 짧은 막대가 1 쪽입니다.',
  'idempotency_key 는 별도 저장소 없이 notification 의 유니크 제약으로 강제합니다 (ADR 0003).'],
 [(340,152,'수신자당 여러 건','middle'),(205,310,'채널 설정',None),(565,320,'시도 기록',None)], 704)
