import sys; sys.path.insert(0, '/tmp/dg')
from spec import N, E, Z, emit_svg, emit_ex
def both(slug, doc, w, h, title, sub, nodes, edges, zones=(), notes=(), labels=(), seed=1):
    P = 'projects/notify-hub/diagrams/%s/diagram' % slug
    emit_svg(P+'.html', doc, w, h, title, sub, nodes, edges, zones, notes, labels)
    print(slug, emit_ex(P+'.excalidraw', title, sub, nodes, edges, zones, notes, labels, seed))

# ── ERD ──
both('notify-erd','알림 도메인 ERD',1080,720,'알림 도메인 ERD',
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

# ── DFD ──
both('notify-dfd','알림 데이터 흐름 (레벨 1)',1080,840,'알림 데이터 흐름 (레벨 1)',
 '알림 데이터가 어떤 처리를 거쳐 어디에 쌓이는가',
 [N(60,180,180,90,'external','발신 서비스'),
  N(340,170,230,110,'process','1.0 요청 접수',kind='ellipse'),
  N(700,185,240,80,'storage','D1 알림 저장소'),
  N(340,400,230,110,'process','2.0 발송',kind='ellipse'),
  N(700,410,240,90,'neutral','외부 공급자'),
  N(340,630,230,110,'process','3.0 재시도 · 포기',kind='ellipse'),
  N(700,635,240,80,'storage','D2 시도 이력')],
 [E([(240,225),(340,225)],'알림 요청',ly=208),
  E([(570,215),(700,215)],'접수 레코드',ly=198),
  E([(455,280),(455,400)],'발송 대상',lx=520,ly=344),
  E([(570,440),(700,440)],'발송 내용',ly=423),
  E([(700,470),(570,470)],'전송 결과',ly=490),
  E([(455,510),(455,630)],'실패 건',lx=515,ly=574),
  E([(570,675),(700,675)],'시도 기록',ly=658)],
 (),
 ['※ 타원은 처리, D 로 시작하는 사각형은 데이터 저장소, 나머지는 외부 개체입니다.',
  'DFD 는 데이터의 이동만 그립니다 — 재시도를 몇 번 하는지 같은 제어는 상태 전이 쪽에 있습니다.'],
 (), 705)

# ── 네트워크 토폴로지 ──
both('notify-network','알림 허브 네트워크 토폴로지',1180,900,'알림 허브 네트워크 토폴로지',
 '어떤 서브넷에 무엇이 있고, 어디로 나가는가',
 [N(60,265,220,90,'external','사내 서비스망'),
  N(420,270,220,80,'process','수신 API ×2'),
  N(760,270,240,80,'process','발송 워커 ×4'),
  N(420,470,220,90,'storage','이력 DB'),
  N(760,470,240,90,'neutral','SQS VPC 엔드포인트'),
  N(760,680,240,80,'process','NAT 게이트웨이'),
  N(60,680,220,90,'external','푸시 · 이메일 공급자')],
 [E([(280,310),(420,310)],'443',ly=292),
  E([(530,350),(530,470)],'5432',lx=585,ly=414),
  E([(640,330),(700,330),(700,515),(760,515)],'적재',lx=672,ly=320),
  E([(880,470),(880,350)],'선점',lx=935,ly=414),
  E([(1000,310),(1080,310),(1080,720),(1000,720)],'443 아웃바운드',lx=1085,ly=520),
  E([(760,720),(280,720)],'인터넷',ly=703)],
 [Z(320,180,820,640,'VPC 10.20.0.0/16'),
  Z(360,240,740,150,'프라이빗 서브넷 · 앱 10.20.10.0/24'),
  Z(360,440,740,160,'프라이빗 서브넷 · 데이터 10.20.20.0/24'),
  Z(360,650,740,130,'퍼블릭 서브넷 10.20.1.0/24')],
 ['※ 이 서비스는 인터넷에서 들어오는 경로가 없습니다 — 사내 서비스망에서만 요청이 옵니다.',
  '나가는 트래픽만 NAT 를 거쳐 공급자에 닿습니다. 큐는 VPC 엔드포인트로 붙어 인터넷을 타지 않습니다.',
  '발송 워커도 이력 DB 에 5432 로 붙습니다 — 선이 겹쳐 수신 API 경로만 그렸습니다.'],
 (), 706)
