import sys; sys.path.insert(0, '/tmp/dg')
from spec import N, E, Z, emit_svg, emit_ex
def both(slug, doc, w, h, title, sub, nodes, edges, zones=(), notes=(), labels=(), seed=1):
    P = 'projects/notify-hub/diagrams/%s/diagram' % slug
    emit_svg(P+'.html', doc, w, h, title, sub, nodes, edges, zones, notes, labels)
    print(slug, emit_ex(P+'.excalidraw', title, sub, nodes, edges, zones, notes, labels, seed))

# ── 클래스 ──
both('notify-class','알림 도메인 클래스',1080,720,'알림 도메인 클래스',
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

# ── 컴포넌트 ──
both('notify-components','수신 API 컴포넌트',1080,700,'수신 API 컴포넌트',
 '요청 하나가 수신 API 안에서 거치는 부품들',
 [N(350,150,380,70,'input','HTTP Controller',['요청 검증 · 응답']),
  N(350,250,380,70,'process','Idempotency Filter',['멱등키로 중복 걸러내기']),
  N(350,350,380,70,'process','Notification Service',['접수 처리 흐름']),
  N(330,460,200,70,'storage','History Repository'),
  N(560,460,200,70,'storage','Queue Publisher'),
  N(60,455,200,80,'neutral','이력 DB'),
  N(850,455,200,80,'neutral','이벤트 큐')],
 [E([(540,220),(540,250)]),
  E([(540,320),(540,350)]),
  E([(430,420),(430,460)]),
  E([(660,420),(660,460)]),
  E([(330,495),(260,495)]),
  E([(760,495),(850,495)])],
 [Z(300,110,480,470,'수신 API')],
 ['※ 점선 안의 상자가 컴포넌트이고, 바깥 두 개는 이 컴포넌트들이 쓰는 외부 자원입니다.',
  '멱등 필터가 컨트롤러 바로 다음에 오는 것이 ADR 0003 의 ② 에 해당합니다.'],
 (), 702)

# ── 패키지 ──
both('notify-packages','모듈 의존 구조',1080,660,'모듈 의존 구조',
 '따로 배포되는 두 모듈이 하나의 도메인을 공유하는 방식',
 [N(320,120,300,90,'input','notify-api',['배포 단위 · 수신']),
  N(700,120,300,90,'input','notify-worker',['배포 단위 · 발송']),
  N(510,300,300,90,'storage','notify-core',['도메인 · 포트']),
  N(510,460,300,90,'neutral','notify-adapters',['SQS · 공급자 · DB'])],
 [E([(470,210),(600,300)],'«use»',dashed=True,head='open',lx=470,ly=270),
  E([(850,210),(760,300)],'«use»',dashed=True,head='open',lx=880,ly=270),
  E([(660,460),(660,390)],'«use»',dashed=True,head='open',lx=730,ly=430)],
 (),
 ['※ notify-api 와 notify-worker 는 따로 배포되지만 같은 도메인 모듈을 씁니다.',
  'notify-core 에서 나가는 화살표가 없다는 점은 온라인 상점의 domain 과 같은 규칙입니다.'],
 [(400,350,'나가는 의존 없음',None)], 703)
