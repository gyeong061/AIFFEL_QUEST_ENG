# 01. Screen Flow

```
Landing
  ↓
Login (Mock)
  ↓
Basic Information (성별/연령/신장/체중)
  ↓
Measurement Route Selection
  ├─ CENTER → Center Measurement Result Input → Fitness Report
  └─ HOME   → PAR-Q
                ├─ 전체 '아니오' → Home Measurement Guide → Measurement Input → Measurement Progress → Measurement Result → Fitness Report
                └─ 1개 이상 '예' → Center Guidance (자가측정/자동처방/주간루틴 차단, 센터측정입력·영상열람·센터안내는 허용)
```

Fitness Report → Exercise Recommendation → Exercise Video

age(연령) ≥ 65 → 어르신 배터리(5종) 자동 적용
age(연령) < 65 → 성인 배터리(4종) 자동 적용

CENTER/HOME 모두 동일한 리포트·추천 파이프라인을 사용하며, 분기 기준은 `source`가 아니라 `측정된 요인`이다.
