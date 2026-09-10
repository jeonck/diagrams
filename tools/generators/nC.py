import sys; sys.path.insert(0, '/tmp/dg')
from spec import N, E, Z, emit_svg, emit_ex
def both(slug, doc, w, h, title, sub, nodes, edges, zones=(), notes=(), labels=(), seed=1):
    P = 'projects/notify-hub/diagrams/%s/diagram' % slug
    emit_svg(P+'.html', doc, w, h, title, sub, nodes, edges, zones, notes, labels)
    print(slug, emit_ex(P+'.excalidraw', title, sub, nodes, edges, zones, notes, labels, seed))

# ── BPMN ──
both('notify-bpmn','실패 알림 처리 프로세스 (BPMN)',1280,820,'실패 알림 처리 프로세스 (BPMN)',
 'DLQ 로 넘어간 알림을 사람이 판단해 되살리거나 접는 과정',
 [N(190,215,140,100,'neutral','알림 실패',kind='ellipse'),
  N(380,220,200,90,'process','운영자에게 통지'),
  N(860,220,200,90,'process','큐에 재적재'),
  N(1100,225,120,80,'neutral','완료',kind='ellipse'),
  N(220,490,200,90,'process','원인 확인'),
  N(470,470,200,130,'external','재발송할까?',kind='diamond'),
  N(720,490,200,90,'risk','포기 기록')],
 [E([(330,265),(380,265)]),
  E([(480,310),(480,420),(320,420),(320,490)],'레인을 넘음',lx=400,ly=410),
  E([(420,535),(470,535)]),
  E([(570,470),(570,420),(960,420),(960,310)],'예',lx=770,ly=410),
  E([(570,600),(570,640),(820,640),(820,580)],'아니오',lx=650,ly=630),
  E([(1060,265),(1100,265)]),
  E([(920,535),(1160,535),(1160,305)])],
 [Z(150,150,1090,240,'시스템'), Z(150,440,1090,250,'운영자')],
 ['※ 가로 띠가 레인입니다 — 위는 시스템이 자동으로 하는 일, 아래는 사람이 판단하는 일입니다.',
  '레인을 넘는 화살표가 담당이 바뀌는 지점이고, 여기서 일이 멈추면 알림은 DLQ 에 그대로 남습니다.'],
 (), 707)

# ── CI/CD ──
r1 = [('커밋','input','기능 브랜치 push'),('빌드','process','api · worker 동시'),
      ('단위 테스트','process','모듈별 실행'),('이미지 2개 빌드','storage','같은 태그로 push')]
r2 = [('스테이징 배포','process','api · worker 함께'),('통합 테스트','process','큐를 통한 E2E'),
      ('승인','external','사람이 누르는 게이트'),('프로덕션 배포','process','worker 먼저, api 나중')]
X = [60, 330, 600, 870]
nodes, edges = [], []
for i,(t,c,s) in enumerate(r1): nodes.append(N(X[i],150,220,90,c,t,[s]))
for i,(t,c,s) in enumerate(r2): nodes.append(N(X[i],350,220,90,c,t,[s]))
for i in range(3):
    edges.append(E([(X[i]+220,195),(X[i+1],195)]))
    edges.append(E([(X[i]+220,395),(X[i+1],395)]))
edges.append(E([(980,240),(980,290),(170,290),(170,350)],'같은 이미지가 이후 단계로',lx=350,ly=282))
both('notify-cicd','알림 허브 CI/CD 파이프라인',1180,600,'알림 허브 CI/CD 파이프라인',
 '한 커밋에서 두 개의 배포 단위가 함께 나가는 경로', nodes, edges, (),
 ['※ api 와 worker 는 같은 커밋에서 함께 빌드되고 함께 나갑니다 — 버전이 갈리면',
  '큐에 오가는 메시지 형식이 어긋납니다. 프로덕션에서는 worker 를 먼저 올려 새 형식을 읽을 수 있게 합니다.'],
 (), 708)

# ── 값 흐름 ──
stages = [('접수','20ms','—'),('큐 대기','—','1.5초'),('워커 처리','80ms','—'),
          ('공급자 전달','300ms','—'),('단말 도착','—','2초')]
nodes, edges = [], []
for i,(name,pt,wt) in enumerate(stages):
    x = 60 + i*240
    nodes.append(N(x,170,200,110,'process',name,['처리 '+pt,'대기 '+wt]))
    if i: edges.append(E([(x-40,225),(x,225)]))
nodes += [N(60,430,260,100,'storage','처리 시간 합계',['0.4초']),
          N(350,430,260,100,'risk','대기 시간 합계',['3.5초']),
          N(640,430,260,100,'neutral','전체 지연',['3.9초']),
          N(930,430,260,100,'external','흐름 효율',['0.4 ÷ 3.9 = 10%'])]
both('notify-value-stream','알림 한 건의 지연 분해',1260,660,'알림 한 건의 지연 분해',
 '요청이 접수되어 단말에 뜨기까지, 일한 시간과 기다린 시간', nodes, edges, (),
 ['※ 숫자는 설명을 위한 예시 값입니다. 실제 측정치로 바꿔 쓰십시오.',
  '온라인 상점의 값 흐름은 기능 하나의 개발 리드타임이고, 이것은 알림 한 건의 실시간 지연입니다.',
  '지연의 90% 가 대기이고 그 대부분이 단말 도착 — 우리가 줄일 수 있는 구간은 큐 대기 1.5초입니다.'],
 (), 709)
