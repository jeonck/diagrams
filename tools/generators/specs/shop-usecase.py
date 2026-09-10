"""쇼핑몰 유스케이스 — order-platform"""
from _bootstrap import N, E, Z, emit

# ── 유스케이스 ──
zones = [Z(300,120,540,560,'온라인 상점 (시스템 경계)')]
nodes = [
 N(60,290,160,90,'external','고객'),
 N(920,180,160,90,'external','관리자'),
 N(900,540,200,90,'neutral','결제 게이트웨이'),
 N(350,160,240,90,'input','상품 검색',kind='ellipse'),
 N(350,290,240,90,'input','장바구니 담기',kind='ellipse'),
 N(350,420,240,90,'process','주문하기',kind='ellipse'),
 N(350,550,240,90,'process','결제하기',kind='ellipse'),
 N(620,160,200,90,'storage','재고 관리',kind='ellipse'),
]
edges = [
 E([(220,320),(350,210)], head=None),
 E([(220,330),(350,330)], head=None),
 E([(220,345),(350,460)], head=None),
 E([(220,360),(350,590)], head=None),
 E([(920,230),(820,205)], head=None),
 E([(590,595),(900,585)], head=None),
]
emit('order-platform', 'shop-usecase','쇼핑몰 유스케이스',1120,780,'쇼핑몰 유스케이스',
     '누가 이 시스템으로 무엇을 할 수 있는가',
     nodes, edges, zones,
     ['※ 타원은 유스케이스, 바깥 상자는 액터입니다. 점선 안이 우리가 만드는 시스템의 범위입니다.',
      '결제 게이트웨이는 사람이 아니라 시스템이지만, 시스템 밖에서 참여하므로 액터로 둡니다.'],
     [], seed=203)
