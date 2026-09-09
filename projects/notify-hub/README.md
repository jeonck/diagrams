# 알림 허브 (notify-hub)

> 이 저장소의 구조를 보이기 위한 **가상의 프로젝트**입니다. 실제 서비스가 아닙니다.

다른 서비스가 보낸 이벤트를 받아 푸시·이메일·SMS로 내보내는 사내 공용 알림 플랫폼입니다.
[온라인 상점](../order-platform/README.md)이 첫 발신 서비스입니다.

## 설계 완료

대표 종류 15개를 모두 그렸고, 설계 결정 세 건도 모두 `채택됨` 입니다.
`node tools/build-index.mjs` 를 돌려도 남은 산출물이 보고되지 않습니다.

가장 먼저 그려야 할 것으로 꼽았던 [시퀀스 다이어그램](diagrams/notify-sequence/diagram.html)이
[0003 멱등키](decisions/0003-idempotency-key.md)의 질문을 좁혀 줬습니다 —
멱등키가 막는 구간(②)과 막지 못하는 구간이 그림 위에 드러났고, 그 자리에 **워커의
조건부 상태 선점(⑤)** 을 넣는 것으로 결론이 났습니다. 결정이 바뀌자
[시퀀스](diagrams/notify-sequence/diagram.html) ·
[액티비티](diagrams/notify-activity/diagram.html) ·
[ERD](diagrams/notify-erd/diagram.html)가 따라 바뀌었습니다.

다만 **"정확히 한 번"은 아닙니다.** 공급자가 요청을 받았지만 결과를 기록하기 전에
워커가 죽는 창이 남아 있고, 공급자 멱등키를 지원하지 않는 채널에서는 중복이 나갈 수
있습니다. 감수하기로 한 것이고, ADR 에 그렇게 적혀 있습니다.

## 범위

**포함** — 알림 요청 접수, 채널별 발송(푸시·이메일·SMS), 재시도와 포기, 발송 이력,
사용자별 채널 설정

**제외** — 알림 문구 작성 도구, A/B 테스트, 발송량 과금, 사용자 세그먼트

## 설계 결정

- **수신과 발송 사이에 큐를 둔다** — 발신 서비스가 공급자 속도에 묶이지 않게 합니다.
  [ADR 0001](decisions/0001-queue-between-receive-and-send.md) ·
  [C4](diagrams/notify-c4/diagram.html)
- **재시도는 지수 백오프로 5회, 그 뒤 DLQ** — 일시 오류는 스스로 회복하고,
  영구 실패는 워커를 붙잡지 않게 합니다.
  [ADR 0002](decisions/0002-retry-with-backoff-then-dlq.md) ·
  [상태 전이](diagrams/notify-state/diagram.html)
- **멱등키로 중복 발송을 막는다** — 수신 단계는 유니크 제약으로, 워커 단계는 조건부
  상태 선점으로 막습니다. 새 저장소는 두지 않습니다.
  [ADR 0003](decisions/0003-idempotency-key.md) ·
  [발송 시퀀스](diagrams/notify-sequence/diagram.html) ·
  [재시도 액티비티](diagrams/notify-activity/diagram.html)
