import sys; sys.path.insert(0, '/tmp/dg')
from ex import Doc, BLUE, PURPLE, TEAL, AMBER, GREY, RED

# ── ERD ──
d = Doc()
d.note('t', '주문 도메인 ERD', 60, 40, 28)
d.note('s', '고객이 주문을 내고, 주문이 항목과 결제로 갈라지는 관계', 60, 78, 16, '#5b6475')
d.link('r1', [[280, 210], [380, 210]], '1 : N', head=None)
d.link('r2', [[600, 210], [700, 210]], '1 : 1', head=None)
d.link('r3', [[490, 300], [490, 420]], '1 : N', head=None)
d.link('r4', [[600, 490], [700, 490]], 'N : 1', head=None)
d.rect('e1', 60, 140, 220, 140, TEAL, '고객\nPK 고객_id\n이메일\n이름')
d.rect('e2', 380, 140, 220, 160, PURPLE, '주문\nPK 주문_id\nFK 고객_id\n주문일시\n상태')
d.rect('e3', 700, 140, 220, 140, PURPLE, '결제\nPK 결제_id\nFK 주문_id\n금액')
d.rect('e4', 380, 420, 220, 160, PURPLE, '주문항목\nPK 주문항목_id\nFK 주문_id\nFK 상품_id\n수량')
d.rect('e5', 700, 420, 220, 140, TEAL, '상품\nPK 상품_id\n이름\n단가')
d.note('n', '※ 청록은 스스로 존재하는 마스터 데이터, 보라는 거래가 생겨야 만들어지는 개체입니다.\n'
            '관계 옆 숫자는 카디널리티입니다 (SVG 버전은 까마귀발로 그렸습니다).', 60, 630, 16, '#5b6475')
print('order-erd', d.save('diagrams/order-erd/diagram.excalidraw'))

# ── 배포 구성 ──
d = Doc(20260910)
d.note('t', '웹 서비스 배포 구성', 60, 40, 28)
d.note('s', '요청이 엣지를 지나 앱 계층에 닿고, 읽기와 쓰기가 갈라지는 지점', 60, 78, 16, '#5b6475')
d.rect('z1', 80, 214, 820, 130, "transparent", dashed=True)
d.rect('z2', 80, 396, 820, 310, "transparent", dashed=True)
d.link('a1', [[440, 200], [230, 244]], '정적 자산')
d.link('a2', [[600, 200], [750, 244]], 'API 요청')
d.link('a3', [[750, 324], [740, 424]], '분배')
d.link('a4', [[620, 464], [340, 464]], '조회 · 세션')
d.link('a5', [[680, 514], [430, 604]], '쓰기')
d.link('a6', [[740, 514], [730, 604]], '읽기')
d.link('a7', [[540, 644], [620, 644]], '복제', dashed=True)
d.rect('n1', 410, 120, 220, 80, AMBER, '브라우저\n사용자 단말')
d.rect('n2', 120, 244, 220, 80, AMBER, 'CDN\n정적 자산 · 캐시')
d.rect('n3', 640, 244, 220, 80, PURPLE, '로드 밸런서\nTLS 종료 · 헬스체크')
d.rect('n4', 620, 424, 240, 90, PURPLE, '앱 서버 ×3\n무상태 · 오토스케일')
d.rect('n5', 120, 424, 220, 80, TEAL, '캐시 (Redis)\n세션 · 조회 결과')
d.rect('n6', 320, 604, 220, 80, TEAL, 'DB Primary\n단일 쓰기 지점')
d.rect('n7', 620, 604, 220, 80, TEAL, 'DB Replica\n읽기 전용 사본')
d.note('z1t', '퍼블릭 구간', 90, 190, 16, '#5b6475')
d.note('z2t', '프라이빗 서브넷', 90, 372, 16, '#5b6475')
d.note('n', '※ 점선 사각형은 신뢰 경계입니다. 앱 서버는 상태를 갖지 않으므로 대수만 늘리면 확장됩니다.', 60, 740, 16, '#5b6475')
print('deployment', d.save('diagrams/deployment-topology/diagram.excalidraw'))

# ── CI/CD ──
d = Doc(20260911)
X = [60, 300, 540, 780]
d.note('t', 'CI/CD 파이프라인', 60, 40, 28)
d.note('s', '커밋 한 번이 프로덕션에 닿기까지 거치는 관문', 60, 78, 16, '#5b6475')
for i in range(3):
    d.link('h%d' % i, [[X[i] + 200, 185], [X[i + 1], 185]])
    d.link('k%d' % i, [[X[i] + 200, 425], [X[i + 1], 425]])
d.link('wrap', [[880, 230], [880, 300], [160, 300], [160, 380]], '같은 이미지가 이후 모든 단계로')
d.link('f1', [[400, 470], [400, 560]], '실패', dashed=True)
d.link('f2', [[880, 470], [880, 600], [740, 600]], '배포 실패', dashed=True)
r1 = [('커밋\n기능 브랜치 push', BLUE), ('빌드\n의존성 · 컴파일', PURPLE),
      ('단위 테스트\n린트 · 커버리지', PURPLE), ('이미지 빌드\n레지스트리에 태그', TEAL)]
r2 = [('스테이징 배포\n프로덕션과 같은 구성', PURPLE), ('통합 테스트\nE2E · 스모크', PURPLE),
      ('승인\n사람이 누르는 게이트', AMBER), ('프로덕션 배포\n롤링 · 헬스체크', PURPLE)]
for i, (label, bg) in enumerate(r1):
    d.rect('s%d' % i, X[i], 140, 200, 90, bg, label)
for i, (label, bg) in enumerate(r2):
    d.rect('u%d' % i, X[i], 380, 200, 90, bg, label)
d.rect('rb', 300, 560, 440, 80, RED, '중단 후 직전 이미지로 롤백\n실패한 커밋은 프로덕션에 도달하지 않습니다')
d.note('n', '※ 실선은 성공 경로, 점선은 실패 경로입니다. 승인만 사람이 누르고 나머지는 자동입니다.', 60, 680, 16, '#5b6475')
print('cicd', d.save('diagrams/cicd-pipeline/diagram.excalidraw'))
