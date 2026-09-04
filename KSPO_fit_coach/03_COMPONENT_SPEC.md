# 03. Component Spec

- `AppShell` — 상단 진행 스텝 표시 + 페이지 컨테이너
- `Stepper` — 현재 플로우 상 위치 표시(진행률)
- `RouteCard` — CENTER/HOME 선택 카드
- `ParQItem` — PAR-Q 단일 문항(예/아니오 토글). 문항별 커스텀 위험도 판단 로직 없음(공통 판정만 사용)
- `MeasurementGuideCard` — 항목명/왜/준비물/공간/방법/주의사항/시작 버튼 구조 고정
- `NumericInput` — 단위 표시 + 범위·빈값 검증(정상범위 수치는 `data/mock-data.js`의 검증 스켈레톤에만 존재, 값 자체는 미확정 → BLOCKED)
- `GripModuleToggle` — `equipment_verified` 플래그를 다루는 악력 선택 모듈
- `PercentileRangeBar` — HOME(구간) / CENTER(단일) 두 가지 렌더 모드, `참고값` 배지 지원(3m 표적 돌아오기 전용)
- `UnmeasuredFactorCard` — 미측정 요인(근력/심폐지구력 등) 안내, 절대 0점·추정치로 표시하지 않음
- `RadarProfile` — 측정/미측정을 시각적으로 구분하는 체력 프로필(0점 대체 금지)
- `TrustBadge` — `자가측정 기준` / `센터 측정` 구분 배지
- `RecommendationCard` — 기본 구성 + 약점 가중 구조, `MOCK DATA` 배지 포함
- `MockBadge` / `BlockedBadge` — Mock 데이터·BLOCKED 항목 표시용 공통 배지
- `DisclaimerFooter` — 34번 고지 문구 고정 컴포넌트
