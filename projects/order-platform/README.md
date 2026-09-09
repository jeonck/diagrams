# 온라인 상점 (order-platform)

> 이 저장소의 다이어그램 표기와 구조를 보이기 위한 **가상의 프로젝트**입니다.
> 실제 서비스가 아니고, 숫자와 이름은 설명을 위해 지어낸 것입니다.

고객이 상품을 주문하고 결제하면, 재고를 차감하고 배송까지 이어지는 커머스 백엔드입니다.

## 범위

**포함** — 상품 검색, 장바구니, 주문 생성, 결제 승인, 재고 차감, 배송 위탁, 주문 취소·환불

**제외** — 정산, 프로모션·쿠폰, 고객 상담, 추천, 다국가·다통화

결제와 이메일 발송은 직접 만들지 않고 외부 시스템에 맡깁니다
([C4 컨텍스트·컨테이너](diagrams/c4-container/diagram.html) 참고).

## 설계 결정

각 항목은 [`decisions/`](decisions) 에 ADR 로 남겨 두었습니다.

- **주문은 상태 기계로 다룬다.** 상태를 필드로 두고 곳곳에서 분기하는 대신, 전이와 그 전이를
  일으키는 사건을 명시합니다. [ADR 0001](decisions/0001-order-as-state-machine.md) · [주문 상태 전이](diagrams/order-state/diagram.html)
- **도메인은 아무것도 의존하지 않는다.** 영속성과 외부 API는 도메인이 정의한 포트를
  인프라가 구현합니다. [ADR 0003](decisions/0003-domain-depends-on-nothing.md) · [패키지 의존 구조](diagrams/package-deps/diagram.html)
- **읽기와 쓰기를 나눈다.** 쓰기는 Primary, 조회는 Replica로 보냅니다.
  [ADR 0004](decisions/0004-split-read-and-write.md) · [웹 서비스 배포 구성](diagrams/deployment-topology/diagram.html)
- **승인만 사람이 누른다.** 프로덕션 배포 직전 한 번을 빼고 파이프라인은 전부 자동입니다.
  [ADR 0006](decisions/0006-manual-approval-before-production.md) · [CI/CD 파이프라인](diagrams/cicd-pipeline/diagram.html)

## 같은 주문을 여러 각도에서

이 프로젝트의 다이어그램은 모두 같은 주문 도메인을 그립니다. 그래서 하나를 이해하면
다른 것을 읽기 쉽습니다 — 같은 `주문`이

- [ERD](diagrams/order-erd/diagram.html)에서는 테이블과 외래 키로,
- [클래스 다이어그램](diagrams/order-class/diagram.html)에서는 책임과 합성으로,
- [상태 전이](diagrams/order-state/diagram.html)에서는 상태와 사건으로,
- [BPMN](diagrams/fulfillment-bpmn/diagram.html)에서는 부서를 넘나드는 업무 흐름으로

나타납니다. 전체 목록은 [저장소 README](../../README.md#다이어그램-목록)에 있습니다.
