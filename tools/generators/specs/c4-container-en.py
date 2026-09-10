"""C4 context · container — order-platform-en"""
from _bootstrap import N, E, Z, emit

# ── C4 containers ──
# 'Read · write' 라벨이 영어로 길어져 데이터베이스를 오른쪽으로 30 밀고
# 경계(zone)도 그만큼 넓혔다. 나머지 배치는 원본 그대로.
zones = [Z(340,150,620,400,'Online Store — the system we build')]
nodes = [
 N(60,190,220,100,'external','Customer',['[Person]','Places orders']),
 N(390,190,240,100,'input','Web App',['[Container: SPA]']),
 N(390,370,240,110,'process','API Application',['[Container: Spring]']),
 N(720,370,210,110,'storage','Database',['[Container: PostgreSQL]']),
 N(340,650,250,100,'neutral','Payment Gateway',['[External System]']),
 N(650,650,250,100,'neutral','Email System',['[External System]']),
]
edges = [
 E([(280,240),(390,240)], 'Places order', ly=224),
 E([(510,290),(510,370)], '[JSON/HTTPS]', lx=585, ly=334),
 E([(630,425),(720,425)], None),
 E([(460,480),(460,650)], 'Payment auth [HTTPS]', lx=350, ly=570),
 E([(570,480),(760,650)], 'Order confirmation [SMTP]', lx=840, ly=600),
]
emit('order-platform-en', 'c4-container-en','C4 Context · Container',1120,830,'C4 Context · Container',
     'The containers inside the system boundary, and the people and systems outside it', nodes, edges, zones,
     ['Note: this is the container level (level 2) of C4. Inside the dashed border is what we deploy; outside it is what we do not build.',
      'A container here is not a Docker container — it means “a unit that is deployed and runs on its own”.'],
     [(636,406,'Read · write',None)], seed=603)
