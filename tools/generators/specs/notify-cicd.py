"""알림 허브 CI/CD 파이프라인 — notify-hub"""
from _bootstrap import N, E, Z, emit

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
emit('notify-hub', 'notify-cicd','알림 허브 CI/CD 파이프라인',1180,600,'알림 허브 CI/CD 파이프라인',
 '한 커밋에서 두 개의 배포 단위가 함께 나가는 경로', nodes, edges, (),
 ['※ api 와 worker 는 같은 커밋에서 함께 빌드되고 함께 나갑니다 — 버전이 갈리면',
  '큐에 오가는 메시지 형식이 어긋납니다. 프로덕션에서는 worker 를 먼저 올려 새 형식을 읽을 수 있게 합니다.'],
 (), 708)
