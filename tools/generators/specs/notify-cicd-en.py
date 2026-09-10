"""알림 허브 CI/CD 파이프라인 (영문) — notify-hub-en"""
from _bootstrap import N, E, Z, emit

# 'Deploy to production' 이 220 폭에 들어가므로 좌표는 원본 그대로 두었다.
# 긴 라벨은 두 행 사이의 빈 자리로 밀어(lx) 상자와 겹치지 않게 했다.
# ── CI/CD ──
r1 = [('Commit','input','Push to feature branch'),('Build','process','api · worker together'),
      ('Unit tests','process','Per module'),('Build 2 images','storage','Pushed with same tag')]
r2 = [('Deploy to staging','process','api · worker together'),('Integration tests','process','E2E through the queue'),
      ('Approval','external','A human presses it'),('Deploy to production','process','worker first, api after')]
X = [60, 330, 600, 870]
W = 220
nodes, edges = [], []
for i,(t,c,s) in enumerate(r1): nodes.append(N(X[i],150,W,90,c,t,[s]))
for i,(t,c,s) in enumerate(r2): nodes.append(N(X[i],350,W,90,c,t,[s]))
for i in range(3):
    edges.append(E([(X[i]+W,195),(X[i+1],195)]))
    edges.append(E([(X[i]+W,395),(X[i+1],395)]))
edges.append(E([(980,240),(980,290),(170,290),(170,350)],'The same image moves on to the later stages',lx=430,ly=282))
emit('notify-hub-en', 'notify-cicd-en','Notification Hub CI/CD pipeline',1180,600,'Notification Hub CI/CD Pipeline',
 'How one commit ships two deployment units together', nodes, edges, (),
 ['Note: api and worker are built from the same commit and ship together — if their versions drift apart,',
  'the message format on the queue no longer lines up. In production the worker goes first, so it can already read the new format.'],
 (), 1208)
