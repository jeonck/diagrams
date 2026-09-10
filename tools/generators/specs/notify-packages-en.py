"""Module dependencies — notify-hub-en"""
from _bootstrap import N, E, Z, emit

# ── packages ──
# 'No outgoing dependencies' 는 한국어 원본보다 길어 왼쪽 정렬(x=400)로 두면 notify-core
# 상자를 파고든다. 오른쪽 끝을 상자 왼쪽 변(510) 앞에 맞추도록 end 정렬(x=494)로 바꿨다.
# 상자 좌표는 원본 그대로.
emit('notify-hub-en', 'notify-packages-en','Module Dependencies',1080,660,'Module Dependencies',
 'How two separately deployed modules share a single domain',
 [N(320,120,300,90,'input','notify-api',['Deployment unit · Intake']),
  N(700,120,300,90,'input','notify-worker',['Deployment unit · Send']),
  N(510,300,300,90,'storage','notify-core',['Domain · Ports']),
  N(510,460,300,90,'neutral','notify-adapters',['SQS · Providers · DB'])],
 [E([(470,210),(600,300)],'«use»',dashed=True,head='open',lx=470,ly=270),
  E([(850,210),(760,300)],'«use»',dashed=True,head='open',lx=880,ly=270),
  E([(660,460),(660,390)],'«use»',dashed=True,head='open',lx=730,ly=430)],
 (),
 ['Note: notify-api and notify-worker are deployed separately but use the same domain module.',
  'No arrow leaves notify-core — the same rule as the domain package in the online store.'],
 [(494,350,'No outgoing dependencies','end')], 1203)
