import sys; sys.path.insert(0, '/tmp/dg')
from seq import build
P = 'projects/notify-hub/diagrams/notify-sequence/diagram'
U, A, Q, W, S = 130, 410, 690, 970, 1250
n = build(P + '.html', P + '.excalidraw', '알림 발송 시퀀스', 1380, 900,
  '알림 발송 시퀀스', '요청 한 건이 접수되어 공급자에게 나가기까지, 그리고 중복이 걸러지는 지점',
  [(U,'external','주문 플랫폼','발신 서비스'),
   (A,'input','수신 API','즉시 응답'),
   (Q,'storage','이벤트 큐','적어도 한 번 전달'),
   (W,'process','발송 워커','재시도 담당'),
   (S,'neutral','푸시 공급자','외부 시스템')],
  [(210,U,A,'① POST /notifications (Idempotency-Key)',False),
   (330,A,Q,'③ 큐에 적재',False),
   (375,A,U,'202 Accepted',True),
   (425,Q,W,'④ 메시지 수신',False),
   (535,W,S,'⑥ 발송 요청 (같은 멱등키 동봉)',False),
   (580,S,W,'200 OK',True),
   (630,W,Q,'⑦ ack — 큐에서 삭제',False)],
  [(A,255,290,'② 멱등키 확인'),(W,465,500,'⑤ 상태 선점 (조건부 UPDATE)')],
  [(U,210,375,'external'),(A,210,375,'input'),(Q,330,630,'storage'),
   (W,425,630,'process'),(S,535,580,'neutral')],
  ['※ 수신 API 는 큐에 넣기만 하고 곧바로 202 를 돌려줍니다 — 발송 결과를 기다리지 않습니다.',
   '② 는 수신 단계의, ⑤ 는 워커 단계의 중복을 막습니다 (ADR 0003). ⑤ 에서 갱신된 행이 0이면',
   '다른 워커가 이미 가져간 것이므로 조용히 넘어갑니다.',
   '⑥ 이후 결과를 기록하기 전에 워커가 죽으면 중복이 남을 수 있어, 공급자에도 같은 키를 보냅니다.'], 501)
print('excalidraw elements:', n)
