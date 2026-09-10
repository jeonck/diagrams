"""알림 도메인 클래스 — notify-hub"""
from _bootstrap import N, E, Z, emit

# ── 클래스 ──
emit('notify-hub', 'notify-class','알림 도메인 클래스',1080,720,'알림 도메인 클래스',
 '알림 한 건과 그것을 보내는 채널, 시도 기록의 관계',
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
 ['※ 속이 찬 마름모는 합성입니다 — 알림이 사라지면 그 시도 기록도 함께 사라집니다.',
  'Channel 은 추상 클래스이고 PushChannel · EmailChannel 이 그것을 구현합니다 (푸시만 그렸습니다).'],
 [(310,170,'1',None),(382,170,'0..*','end'),(542,410,'1..*',None),(680,170,'1',None),(752,170,'0..*','end')], 701)
