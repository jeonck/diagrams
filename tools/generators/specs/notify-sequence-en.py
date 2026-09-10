"""Notification send sequence — notify-hub-en"""
from _bootstrap import emit_seq

# 참여자 간격(280)과 메시지 y 좌표는 원본 그대로다.
# 영어 라벨이 길어지는 곳은 좌표 대신 문구를 줄였다:
#   ⑤ 는 '⑤ Claim (conditional UPDATE)' 로, ⑥ 은 괄호를 짧게 잡아
#   자기 메시지 라벨(cx+78)이 오른쪽 생명선(1250)을 넘지 않게 했다.
U, A, Q, W, S = 130, 410, 690, 970, 1250

emit_seq('notify-hub-en', 'notify-sequence-en',
  'Notification Send Sequence', 1380, 900,
  'Notification Send Sequence', 'One request from intake out to the provider, and where duplicates are filtered out',
  [(U,'external','Order platform','Sending service'),
   (A,'input','Intake API','Responds at once'),
   (Q,'storage','Event queue','At-least-once delivery'),
   (W,'process','Send worker','Owns retries'),
   (S,'neutral','Push provider','External system')],
  [(210,U,A,'① POST /notifications (Idempotency-Key)',False),
   (330,A,Q,'③ Put on the queue',False),
   (375,A,U,'202 Accepted',True),
   (425,Q,W,'④ Receive message',False),
   (535,W,S,'⑥ Send request (same idempotency key)',False),
   (580,S,W,'200 OK',True),
   (630,W,Q,'⑦ ack — remove from queue',False)],
  [(A,255,290,'② Check idempotency key'),(W,465,500,'⑤ Claim (conditional UPDATE)')],
  [(U,210,375,'external'),(A,210,375,'input'),(Q,330,630,'storage'),
   (W,425,630,'process'),(S,535,580,'neutral')],
  ['Note: the Intake API only puts the event on the queue and returns 202 right away — it does not wait for the send result.',
   '② guards the intake stage and ⑤ guards the worker stage (ADR 0003). If the UPDATE at ⑤ changes 0 rows,',
   'another worker already took the message, so this one moves on quietly.',
   'If the worker dies after ⑥ but before the result is recorded, a duplicate can still go out — so the provider gets the same key too.'], seed=1001)
