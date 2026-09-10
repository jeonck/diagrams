"""CI/CD 파이프라인 (영문) — order-platform-en"""
from _bootstrap import N, E, Z, emit

nodes = [
 N(40,140,190,72,'input','Commit',['Push to feature branch']),
 N(270,140,190,72,'process','Build',['Dependencies · Compile']),
 N(500,140,190,72,'process','Unit Tests',['Lint · Coverage']),
 N(730,140,190,72,'storage','Image Build',['Tagged in registry']),
 N(40,330,190,72,'process','Staging Deploy',['Same config as prod']),
 N(270,330,190,72,'process','Integration Tests',['E2E · Smoke']),
 N(500,330,190,72,'external','Approval',['A human presses this']),
 N(730,330,190,72,'process','Production Deploy',['Rolling · Health check']),
 # 라벨이 있는 도형이므로 120x60 이상 (규칙) — 420x60
 N(270,450,420,60,'risk','Halt and roll back to previous image',['A failed commit never reaches production']),
]
edges = [
 E([(230,176),(270,176)]),
 E([(230,366),(270,366)]),
 E([(460,176),(500,176)]),
 E([(460,366),(500,366)]),
 E([(690,176),(730,176)]),
 E([(690,366),(730,366)]),
 E([(825,212),(825,268),(135,268),(135,330)]),
 E([(365,402),(365,450)], dashed=True),
 E([(825,402),(825,480),(690,480)], dashed=True),
]
labels = [
 (145,262,'The same image flows on through every later stage',None),
 (375,440,'Fail',None),
 (700,440,'Deploy failed','end'),
]
emit('order-platform-en', 'cicd-pipeline-en', 'CI/CD pipeline', 940, 600,
     'CI/CD Pipeline', 'The gates one commit passes through on its way to production',
     nodes, edges, (),
     ['Note: Solid lines are the success path, dashed lines the failure path. Only the approval is human; the rest is automatic.'],
     labels, seed=803)
