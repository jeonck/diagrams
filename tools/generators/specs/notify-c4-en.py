"""Notification Hub C4 context · container — notify-hub-en"""
from _bootstrap import N, E, Z, emit

# ── C4 containers ──
# 'Push · Email Providers' 가 원본 상자(w=220)를 넘쳐 x 를 900 으로 당기고 w 를 270 으로
# 넓혔다 (오른쪽 여백 30 확보). 그에 맞춰 발송 화살표의 끝점도 940 → 900.
# 'Notification request' 라벨은 두 상자 사이 90px 틈보다 길어, 점선 경계를 넘지 않도록
# 왼쪽·위(lx=250, ly=212)로 밀어 발신 서비스 상자 위쪽 빈 자리에 놓았다.
# 'Record result' 는 'Send [HTTPS]' 와 붙어 보여 12 만큼 왼쪽으로 뺐다.
emit('notify-hub-en', 'notify-c4-en','Notification Hub C4 Context · Container',1200,780,
 'Notification Hub — C4 Context · Container',
 'The containers inside the system boundary, and the senders and providers outside it',
 [N(60,220,220,100,'external','Sending Service',['[External System]','e.g. order platform']),
  N(370,200,240,100,'input','Intake API',['[Container: Spring]']),
  N(370,360,240,90,'storage','Event Queue',['[Container: SQS]']),
  N(370,500,240,100,'process','Send Worker',['[Container: Spring]']),
  N(650,360,200,90,'storage','History DB',['[Container: PostgreSQL]']),
  N(900,500,270,100,'neutral','Push · Email Providers',['[External System]'])],
 [E([(280,270),(370,250)],'Notification request',lx=250,ly=212),
  E([(490,300),(490,360)],'Enqueue',lx=545,ly=334),
  E([(490,450),(490,500)],'Claim',lx=540,ly=478),
  E([(610,250),(700,360)],'Record intake',lx=725,ly=296),
  E([(560,500),(700,450)],'Record result',lx=660,ly=506),
  E([(610,540),(900,540)],'Send [HTTPS]',ly=522)],
 [Z(320,150,560,470,'Notification Hub — the system we build')],
 ['Note: the Intake API only puts the event on the queue and returns 202 right away. The worker does the sending separately.',
  'The sending service never waits for a slow provider — the queue keeps the two apart.'],
 (), 903)
