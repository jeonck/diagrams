"""MVC request sequence — order-platform-en"""
from _bootstrap import emit_seq

# Participant spacing matches the notification-hub sequence so the two grids line up
U, C, M, R, V = 130, 410, 690, 970, 1250

emit_seq('order-platform-en', 'mvc-sequence-en', 'MVC Request Sequence', 1380, 740,
  'MVC Request Sequence', 'One create-order request through each role and back as a response',
  [(U,'input','User','Browser'),
   (C,'process','Controller','Handles request'),
   (M,'storage','Model','Domain logic'),
   (R,'neutral','Repository','Persistence'),
   (V,'external','View','Rendering')],
  [(220,U,C,'① POST /orders',False),
   (327,C,M,'③ createOrder(cmd)',False),
   (371,M,R,'④ save(order)',False),
   (411,R,M,'order #1024',True),
   (451,M,C,'Order',True),
   (495,C,V,'⑤ render(order)',False),
   (535,V,C,'HTML',True),
   (575,C,U,'200 OK + HTML',True)],
  [(C,263,289,'② Validate input')],
  [(U,222,573,'input'),(C,222,573,'process'),(M,315,435,'storage'),
   (R,373,409,'neutral'),(V,497,533,'external')],
  ['Note: solid lines are calls, dashed lines are returns. A vertical bar marks the stretch where a participant is working.',
   'The Repository is grey because it is not one of the three MVC roles — it is what the Model hands persistence to.'],
  seed=804)
