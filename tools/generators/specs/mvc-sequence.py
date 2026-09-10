"""MVC 요청 시퀀스 — order-platform"""
from _bootstrap import emit_seq

# 참여자 간격은 알림 허브 시퀀스와 같게 두어 두 그림의 눈금이 맞는다
U, C, M, R, V = 130, 410, 690, 970, 1250

emit_seq('order-platform', 'mvc-sequence', 'MVC 요청 처리 시퀀스', 1380, 740,
  'MVC 요청 처리 시퀀스', '주문 생성 요청 한 건이 각 역할을 거쳐 응답으로 돌아오기까지',
  [(U,'input','사용자','브라우저'),
   (C,'process','Controller','요청 처리'),
   (M,'storage','Model','도메인 로직'),
   (R,'neutral','Repository','영속성'),
   (V,'external','View','렌더링')],
  [(220,U,C,'① POST /orders',False),
   (327,C,M,'③ createOrder(cmd)',False),
   (371,M,R,'④ save(order)',False),
   (411,R,M,'order #1024',True),
   (451,M,C,'Order',True),
   (495,C,V,'⑤ render(order)',False),
   (535,V,C,'HTML',True),
   (575,C,U,'200 OK + HTML',True)],
  [(C,263,289,'② 입력 검증')],
  [(U,222,573,'input'),(C,222,573,'process'),(M,315,435,'storage'),
   (R,373,409,'neutral'),(V,497,533,'external')],
  ['※ 실선은 호출, 점선은 반환입니다. 세로 막대는 각 참여자가 처리 중인 구간을 뜻합니다.',
   'Repository는 MVC의 세 역할이 아니라 Model이 영속성을 맡길 대상이라 회색으로 두었습니다.'],
  seed=304)
