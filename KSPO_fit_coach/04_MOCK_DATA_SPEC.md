# 04. Mock Data Spec

모든 Mock 데이터는 `mockXxx` 네이밍과 `MOCK DATA` 표기로 실제 데이터와 구분한다.

## measurement (스키마, §21 기준)
```
measurement_id, user_id, item_code, raw_value, source(CENTER|HOME),
protocol_match, equipment_verified, percentile_eligible,
norm_version_used, measured_at
```

## mockUser
```
{ gender, ageBand(5세 단위), height, weight }
```

## mockHomeBattery
```
adult: [BMI, cross_situp, sit_and_reach, standing_long_jump]
senior: [BMI, chair_stand, sit_and_reach, two_min_step, chair_sit_and_reach_3m]
```
근력/심폐지구력(성인), 상지 근기능/협응력(어르신)은 배터리에 없음 → `측정하지 않음` 상태만 존재.

## mockPercentileRanges (§11 예시값, MOCK)
```
standing_long_jump: ±5%p
cross_situp: ±7%p
sit_and_reach: ±10%p
two_min_step: ±7%p
chair_stand: ±5%p
chair_sit_and_reach_3m: 참고값(구간 폭 미확정)
```
실제 계산 공식·규준 데이터는 연결 전까지 이 예시 구간만 사용(§18, §20 원칙 그대로 유지: 다년도 풀링 2022.01~2026.07, 절대악력 규준은 2024년 이후만).

## mockExerciseRecommendation
기본 구성 + 약점 가중 구조의 예시 텍스트만 포함. 실제 종목-요인 매핑 데이터 연결 전까지 `MOCK DATA`로 표기.

## mockNormVersion
`norm_version_used` 플레이스홀더 문자열만 사용, 실제 버전 미확정.
