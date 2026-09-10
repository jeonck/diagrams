"""실패 알림 처리 프로세스 (BPMN, 영문) — notify-hub-en"""
from _bootstrap import N, E, Z, emit

# ── BPMN ──
# 영어 라벨이 길어 시작 이벤트 타원(140 → 190)과 재적재 상자(200 → 220)를 넓히고,
# 그에 맞춰 연결선의 시작·끝점을 옮겼다. 레인과 배치 뼈대는 원본 그대로다.
emit('notify-hub-en', 'notify-bpmn-en','Failed Notification Handling (BPMN)',1280,820,
 'Failed Notification Handling (BPMN)',
 'How a person decides to requeue or give up on a notification that fell into the DLQ',
 [N(165,215,190,100,'neutral','Notification failed',kind='ellipse'),
  N(380,220,200,90,'process','Notify operator'),
  N(860,220,220,90,'process','Requeue notification'),
  N(1100,225,120,80,'neutral','Done',kind='ellipse'),
  N(220,490,200,90,'process','Check the cause'),
  N(470,470,200,130,'external','Resend?',kind='diamond'),
  N(720,490,200,90,'risk','Record as given up')],
 [E([(355,265),(380,265)]),
  E([(480,310),(480,420),(320,420),(320,490)],'crosses the lane',lx=400,ly=410),
  E([(420,535),(470,535)]),
  E([(570,470),(570,420),(970,420),(970,310)],'Yes',lx=770,ly=410),
  E([(570,600),(570,640),(820,640),(820,580)],'No',lx=650,ly=630),
  E([(1080,265),(1100,265)]),
  E([(920,535),(1160,535),(1160,305)])],
 [Z(150,150,1090,240,'System'), Z(150,440,1090,250,'Operator')],
 ['Note: the horizontal bands are lanes — the top one is what the system does on its own, the bottom one is where a person decides.',
  'An arrow crossing a lane is where ownership changes, and if the work stops there the notification just sits in the DLQ.'],
 (), 1207)
