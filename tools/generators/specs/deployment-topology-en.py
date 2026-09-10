"""웹 서비스 배포 구성 (영문) — order-platform-en"""
from _bootstrap import N, E, Z, emit

# 영어 라벨이 길어 로드 밸런서 상자를 240 으로 넓히고(중심 x 는 원본 그대로),
# 'Replication' 이 들어가도록 두 DB 상자 사이 간격을 60 → 100 으로 벌렸다.
zones = [
 Z(60,176,820,112,'Public zone'),
 Z(60,316,820,330,'Private subnet'),
]
nodes = [
 N(380,88,180,60,'external','Browser',['User device']),
 N(150,200,200,68,'external','CDN',['Static assets · Cache']),
 N(580,200,240,68,'process','Load Balancer',['TLS termination · Health checks']),
 # 앞 상자보다 먼저 그려 “여러 대” 를 겹친 그림자로 표현한다
 N(570,368,220,68,'process',None),
 N(562,360,220,68,'process','App Servers ×3',['Stateless · Autoscaled']),
 N(170,362,200,68,'storage','Cache (Redis)',['Sessions · Query results']),
 N(280,526,200,72,'storage','DB Primary',['Single write point']),
 N(580,526,200,72,'storage','DB Replica',['Read-only copy']),
]
edges = [
 E([(420,148),(250,200)]),
 E([(520,148),(690,200)]),
 E([(700,268),(670,356)]),
 E([(560,396),(370,396)]),
 E([(640,436),(410,526)]),
 E([(680,436),(675,526)]),
 E([(480,562),(580,562)], dashed=True),
]
labels = [
 (300,142,'Static assets','middle'),
 (645,142,'API requests','middle'),
 (718,330,'Distribute','middle'),
 (465,388,'Lookup · Session','middle'),
 (462,480,'Write','middle'),
 (706,480,'Read','middle'),
 (530,552,'Replication','middle'),
]
emit('order-platform-en', 'deployment-topology-en', 'Web service deployment', 940, 780,
     'Web Service Deployment',
     'How a request crosses the edge into the app tier, and where reads split from writes',
     nodes, edges, zones,
     ['Note: The dashed rectangles are trust boundaries. Only the public zone is reachable directly from the internet; the private subnet is not.',
      'App servers hold no state, so scaling means adding instances; sessions live in the cache and data in the database.'],
     labels, seed=802)
