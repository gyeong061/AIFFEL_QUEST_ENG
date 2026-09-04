# 05. API Placeholder

Backend API가 미확정이므로 Request/Response 스키마를 임의 확정하지 않는다. 아래는 인터페이스 자리표시(placeholder)이며 실제 연동 시 재정의가 필요하다.

```js
// services/api.js
// TODO: Backend API schema confirmation required (Request/Response 미확정)

export async function submitMeasurement(payload) {
  // payload: measurement 구조(§21)를 따를 예정, 필드 확정 필요
  throw new Error("API not connected — placeholder only");
}

export async function fetchPercentileReport(measurementId) {
  // Response 구조 미확정 — 확정 전까지 mock-data.js 사용
  throw new Error("API not connected — placeholder only");
}

export async function fetchExerciseRecommendation(userId, weakFactors) {
  throw new Error("API not connected — placeholder only");
}
```

실제 연동 전까지 모든 화면은 `data/mock-data.js`만 참조한다.
