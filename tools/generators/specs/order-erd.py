"""주문 도메인 ERD — order-platform"""
from _bootstrap import N, E, Z, emit

nodes = [
 N(60,110,200,126,'storage','고객',kind='entity',attrs=['PK  고객_id','이메일','이름']),
 N(370,110,200,148,'process','주문',kind='entity',attrs=['PK  주문_id','FK  고객_id','주문일시','상태']),
 N(680,110,200,126,'process','결제',kind='entity',attrs=['PK  결제_id','FK  주문_id','금액']),
 N(370,390,200,148,'process','주문항목',kind='entity',attrs=['PK  주문항목_id','FK  주문_id','FK  상품_id','수량']),
 N(680,390,200,126,'storage','상품',kind='entity',attrs=['PK  상품_id','이름','단가']),
]
edges = [
 E([(260,173),(370,173)], head='many', start='one-s'),
 E([(570,173),(680,173)], head='one',  start='one-s'),
 E([(470,258),(470,390)], head='many', start='one-s'),
 E([(570,460),(680,460)], head='one',  start='many-s'),
 # 범례 — 까마귀발 표기를 그림 안에서 설명한다
 E([(60,612),(120,612)], head='one'),
 E([(240,612),(300,612)], head='many'),
]
labels = [
 (315,166,'주문한다','middle'),
 (625,166,'결제된다','middle'),
 (482,330,'담는다',None),
 (625,453,'가리킨다','middle'),
 (130,616,'1 (하나)',None),
 (310,616,'N (여럿) — 까마귀발 표기법',None),
]
emit('order-platform', 'order-erd', '주문 도메인 ERD', 940, 700, '주문 도메인 ERD',
     '고객이 주문을 내고, 주문이 항목과 결제로 갈라지는 관계',
     nodes, edges, (),
     ['※ 청록은 스스로 존재하는 마스터 데이터, 남색은 거래가 생겨야 만들어지는 개체입니다.'],
     labels, seed=301)
