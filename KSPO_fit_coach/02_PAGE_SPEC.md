# 02. Page Spec

| # | 페이지 | 핵심 목적 | 주요 상태/분기 |
|---|---|---|---|
| 01 | Landing | 가치 제안 + CTA(체력 측정 시작하기) | - |
| 02 | Login | 로그인 흐름 표현(Mock) | `MOCK` 배지 표시, 실제 인증처럼 보이지 않게 함 |
| 03 | Basic Information | 성별/연령/신장/체중 입력 | 연령으로 성인/어르신 자동 분기 |
| 04 | Measurement Route Selection | CENTER vs HOME 선택 | 선택값이 `measurement.source`로 저장 |
| 05 | PAR-Q | 7문항 예/아니오 | 1개 이상 '예' → 자가측정 차단 분기 |
| 06 | Home Measurement Guide | 항목별 왜/준비물/공간/방법/주의사항 안내 | 성인 4종 / 어르신 5종, 악력 선택 모듈 |
| 07 | Measurement Input | 결과 숫자 입력(단위 표시) | 범위/빈값 검증만 수행(정상범위 수치는 임의 결정 금지 → BLOCKED 배지) |
| 08 | Measurement Progress | 진행률 표시 | 순차 진행 애니메이션 |
| 09 | Measurement Result | 입력값 확인 | 리포트로 이동 |
| 10 | Fitness Report | 나의 결과/또래비교/강점·약점/미측정/운동추천/센터안내 | HOME=구간 백분위, CENTER=단일 값, 인증등급 미표시 |
| 11 | Exercise Recommendation | 기본구성 + 약점가중 추천 | source 무관 동일 파이프라인, `MOCK DATA` 배지 |
| 12 | Exercise Video | 국민체력100 공식 콘텐츠 영상 목록(Mock) | - |
| 13 | Center Measurement Result Input | 센터 측정값 직접 입력 | 신뢰도 표기 `센터 측정` |
| 14 | Center Guidance | 체력인증센터 안내(PAR-Q 미통과 포함) | 자가측정/자동처방/주간루틴 차단, 공단 영상열람·센터안내는 허용 |

공통: 모든 리포트/결과 화면 하단에 34번 항목의 고지 문구를 고정 표시.
