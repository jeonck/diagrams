"""알림 도메인 클래스 (영문) — notify-hub-en"""
from _bootstrap import N, E, Z, emit

# ── 클래스 ──
# 클래스 이름·속성·메서드는 이미 영문 카멜케이스라 좌표를 그대로 쓴다 (제목/부제/각주만 옮김).
emit('notify-hub-en', 'notify-class-en','Notification Domain Classes',1080,720,'Notification Domain Classes',
 'How one notification relates to the channel that sends it and to its delivery attempts',
 [N(60,110,240,134,'storage','Recipient',kind='class',attrs=['- userId: Long','- locale: Locale'],ops=['+ channelsFor(t): List']),
  N(390,110,280,174,'process','Notification',kind='class',attrs=['- id: Long','- idempotencyKey: String','- status: Status'],ops=['+ markSent(): void','+ fail(reason): void']),
  N(760,110,240,132,'process','Channel',kind='class',stereo='«abstract»',attrs=['- enabled: boolean'],ops=['+ send(msg): Result']),
  N(390,420,280,134,'process','DeliveryAttempt',kind='class',attrs=['- attemptNo: int','- at: Instant'],ops=['+ isRetryable(): boolean']),
  N(760,420,240,114,'process','PushChannel',kind='class',attrs=['- deviceToken: String'],ops=['+ send(msg): Result'])],
 [E([(300,177),(390,177)], head=None),
  E([(530,284),(530,420)], head=None, start='diamond'),
  E([(670,177),(760,177)], head=None),
  E([(880,420),(880,242)], head='tri')],
 (),
 ['Note: the filled diamond is composition — when a Notification goes away, its delivery attempts go with it.',
  'Channel is an abstract class, and PushChannel and EmailChannel implement it (only push is drawn here).'],
 [(310,170,'1',None),(382,170,'0..*','end'),(542,410,'1..*',None),(680,170,'1',None),(752,170,'0..*','end')], 1201)
