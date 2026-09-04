const { createApp, reactive, computed } = Vue;

/* ============================================================
   MOCK DATA
   ============================================================ */

const ADULT_ITEMS = [
  { code: "cross_situp", name: "교차윗몸일으키기", unit: "회", why: "복부·코어 근지구력을 확인해요.", prep: "매트 또는 바닥에 깔 담요", space: "누울 수 있는 1.5m x 1m 공간", method: "무릎을 세우고 누운 뒤, 팔꿈치가 반대쪽 무릎에 닿도록 상체를 교차로 들어올려요.", caution: "목에 힘을 주지 말고 반동을 사용하지 마세요." },
  { code: "sit_and_reach", name: "앉아윗몸앞으로굽히기", unit: "cm", why: "허리·하체 뒤쪽 유연성을 확인해요.", prep: "줄자 또는 유연성 측정자, 벽", space: "다리를 뻗고 앉을 수 있는 공간", method: "다리를 펴고 앉아 상체를 천천히 앞으로 굽혀 손끝이 닿는 위치를 측정해요.", caution: "무릎을 굽히지 말고, 통증이 있으면 즉시 중단하세요.", note: "영점 기준: 발바닥 앞면을 0cm으로 두고, 발끝을 넘으면 +, 못 미치면 −로 기록해요." },
  { code: "standing_long_jump", name: "제자리멀리뛰기", unit: "cm", why: "하체 순발력을 확인해요.", prep: "줄자, 미끄럽지 않은 바닥", space: "착지 거리까지 2m 이상의 평평한 공간", method: "제자리에서 두 발로 최대한 멀리 뛰어 착지 지점까지의 거리를 측정해요.", caution: "착지 시 무릎에 힘을 주고 균형을 잃지 않도록 주의하세요." },
];

const SENIOR_ITEMS = [
  { code: "chair_stand", name: "의자에 앉았다 일어서기", unit: "회", why: "하지 근기능을 확인해요.", prep: "등받이 없는 안정된 의자", space: "의자 앞뒤로 여유 공간", method: "팔짱을 낀 채 정해진 시간 동안 앉았다 일어서기를 반복해요.", caution: "의자가 흔들리지 않는지 먼저 확인하세요.", note: "의자 좌면 높이: 무릎이 90도 정도로 굽혀지는 높이로 통일해야 결과가 일관돼요." },
  { code: "sit_and_reach", name: "앉아윗몸앞으로굽히기", unit: "cm", why: "허리·하체 뒤쪽 유연성을 확인해요.", prep: "줄자 또는 유연성 측정자", space: "다리를 뻗고 앉을 수 있는 공간", method: "다리를 펴고 앉아 상체를 천천히 앞으로 굽혀 손끝이 닿는 위치를 측정해요.", caution: "무릎을 굽히지 말고, 통증이 있으면 즉시 중단하세요.", note: "영점 기준: 발바닥 앞면을 0cm으로 두고, 발끝을 넘으면 +, 못 미치면 −로 기록해요." },
  { code: "two_min_step", name: "2분 제자리걷기", unit: "회", why: "심폐 지구력 관련 기능을 확인해요.", prep: "무릎 높이 표시 테이프", space: "제자리 걷기가 가능한 공간", method: "2분 동안 무릎을 정해진 높이까지 올리며 제자리 걷기를 반복해요.", caution: "어지러움이 느껴지면 즉시 중단하세요." },
  { code: "chair_sit_and_reach_3m", name: "의자에 앉아 3m 표적 돌아오기", unit: "초", why: "민첩성과 균형 관련 기능을 확인해요.", prep: "의자, 표적(콘 등), 줄자", space: "왕복 3m 이상의 통로", method: "의자에서 일어나 3m 앞 표적을 돌아 다시 앉기까지의 시간을 측정해요.", caution: "회전 시 미끄러지지 않도록 주의하세요." },
];

const GRIP_ITEM = { code: "grip_strength", name: "악력", unit: "kg", why: "상지 근력을 확인해요.", prep: "악력계", space: "서서 측정할 수 있는 공간", method: "악력계를 잡고 최대 힘으로 2회 측정해 더 큰 값을 기록해요.", caution: "손목을 비틀지 말고 팔을 몸에서 떨어뜨려 측정하세요." };

const CENTER_EXTRA_ITEMS = [
  { code: "grip_strength", name: "악력", unit: "kg" },
  { code: "cardio_endurance", name: "심폐지구력(센터 측정)", unit: "점" },
];

// PAR-Q — 공단 원문 확정본(사용자 제공, CONFIRMED)
const PARQ_QUESTIONS = [
  "의사에게 심장질환 진단을 받았거나, 신체활동/운동 삼가에 대한 말을 들은 적이 있습니까?",
  "운동을 할 때 가슴에 통증이 있습니까?",
  "지난달 휴식 시에도 가슴에 통증을 느낀 적이 있습니까?",
  "어지럼증으로 쓰러졌거나 의식을 잃은 적이 있습니까?",
  "운동할 때 심해질 수 있는 관절이나 뼈의 문제(예: 허리, 무릎 또는 고관절)가 있습니까?",
  "심장질환 등으로 의사에게 처방 받아 복용하는 약이 있습니까?",
  "신체활동/운동을 해서는 안되는 다른 이유가 있습니까?",
];

const NORM_PERIOD_NOTE = "규준 데이터 기준: 2022.01 ~ 2026.07 다년도 풀링(MOCK)";

const RANGE_WIDTH = { sit_and_reach: 10, cross_situp: 7, two_min_step: 7, standing_long_jump: 5, chair_stand: 5 };

const MOCK_CENTER_PERCENTILE = { cross_situp: 62, sit_and_reach: 68, standing_long_jump: 32, chair_stand: 55, two_min_step: 48, grip_strength: 58 };

function computeRange(code, center) {
  const w = RANGE_WIDTH[code];
  if (w == null) return null;
  const lo = Math.max(1, Math.round(center - w));
  const hi = Math.min(99, Math.round(center + w));
  return [lo, hi];
}

const PROGRESS_MAP = { landing: null, login: null, basicInfo: 10, routeSelect: 20, parq: 30, homeGuide: 42, measureInput: 55, measureProgress: 68, measureResult: 78, report: 88, recommend: 94, video: 100, centerInput: 60, centerGuidance: null };
const TITLE_MAP = { landing: "Landing", login: "Login", basicInfo: "기본정보", routeSelect: "측정 경로", parq: "PAR-Q", homeGuide: "홈 측정 가이드", measureInput: "결과 입력", measureProgress: "분석 중", measureResult: "결과 확인", report: "체력 리포트", recommend: "운동 추천", video: "운동 영상", centerInput: "센터 결과 입력", centerGuidance: "센터 안내" };

/* ============================================================
   VUE APP
   ============================================================ */

const App = {
  data() {
    return {
      page: "landing",
      form: { gender: "", age: "", height: "", weight: "" },
      route: null,
      parqAnswers: Array(7).fill(null),
      parqBlocked: false,
      gripOwned: null,
      homeValues: {},
      centerValues: {},
      openGuideIdx: 0,
      progressPct: 0,
      progressTimer: null,
      parqQuestions: PARQ_QUESTIONS,
      normPeriodNote: NORM_PERIOD_NOTE,
    };
  },
  computed: {
    ageGroup() { return Number(this.form.age) >= 65 ? "senior" : "adult"; },
    battery() { return this.ageGroup === "senior" ? SENIOR_ITEMS : ADULT_ITEMS; },
    homeMeasuredItems() { return [...this.battery, ...(this.gripOwned ? [GRIP_ITEM] : [])]; },
    centerMeasuredItems() { return [...this.battery, ...CENTER_EXTRA_ITEMS]; },
    reportItems() { return this.route === "CENTER" ? this.centerMeasuredItems : this.homeMeasuredItems; },
    reportValues() { return this.route === "CENTER" ? this.centerValues : this.homeValues; },
    basicInfoValid() { return this.form.gender && this.form.age && this.form.height && this.form.weight; },
    parqAnswered() { return this.parqAnswers.every(a => a !== null); },
    homeInputAllFilled() { return this.homeMeasuredItems.every(it => this.homeValues[it.code] !== undefined && this.homeValues[it.code] !== "" && Number(this.homeValues[it.code]) >= 0); },
    centerInputAllFilled() { return this.centerMeasuredItems.every(it => this.centerValues[it.code] !== undefined && this.centerValues[it.code] !== "" && Number(this.centerValues[it.code]) >= 0); },
    unmeasuredList() {
      const list = [];
      if (this.route !== "HOME") return list;
      if (!this.gripOwned) list.push({ label: "근력", note: "악력계가 있으면 측정할 수 있어요." });
      if (this.ageGroup === "adult") list.push({ label: "심폐지구력", note: "가까운 체력인증센터에서 측정할 수 있어요." });
      else list.push({ label: "상지 근기능", note: "가까운 체력인증센터에서 측정할 수 있어요." }, { label: "협응력", note: "가까운 체력인증센터에서 측정할 수 있어요." });
      return list;
    },
    percentileRanked() {
      return this.reportItems
        .filter(it => it.code !== "cardio_endurance")
        .map(it => ({ name: it.name, pct: MOCK_CENTER_PERCENTILE[it.code] ?? 50 }))
        .sort((a, b) => b.pct - a.pct);
    },
    strongest() { return this.percentileRanked[0]; },
    weakest() { return this.percentileRanked[this.percentileRanked.length - 1]; },
    comparisonRows() {
      return this.reportItems
        .filter(it => it.code !== "cardio_endurance")
        .map(it => {
          const center = MOCK_CENTER_PERCENTILE[it.code] ?? 50;
          const topPct = 100 - center;
          const value = this.reportValues[it.code];
          if (this.route === "CENTER") {
            const r = [Math.max(1, topPct - 1), Math.min(99, topPct + 1)];
            return { code: it.code, name: it.name, unit: it.unit, value, mode: "point", text: `또래 상위 ${topPct}%`, range: r };
          }
          if (it.code === "chair_sit_and_reach_3m") {
            return { code: it.code, name: it.name, unit: it.unit, value, mode: "reference", text: "참고값 · 구간 폭 미확정", range: null };
          }
          if (it.code === "grip_strength") {
            const r = [Math.max(1, topPct - 1), Math.min(99, topPct + 1)];
            return { code: it.code, name: it.name, unit: it.unit, value, mode: "point", text: `또래 상위 ${topPct}% · 정식 백분위`, range: r };
          }
          const r = computeRange(it.code, center);
          if (!r) {
            return { code: it.code, name: it.name, unit: it.unit, value, mode: "reference", text: "참고값 · 구간 폭 미확정", range: null };
          }
          return { code: it.code, name: it.name, unit: it.unit, value, mode: "range", text: `또래 상위 ${100 - r[1]}~${100 - r[0]}%`, range: r };
        });
    },
    weakestHomeName() {
      const items = this.homeMeasuredItems.map(it => ({ name: it.name, pct: MOCK_CENTER_PERCENTILE[it.code] ?? 50 }));
      return items.sort((a, b) => a.pct - b.pct)[0]?.name;
    },
    progressLabel() { return TITLE_MAP[this.page]; },
    progressPctBar() { return PROGRESS_MAP[this.page]; },
  },
  methods: {
    go(next) { this.page = next; window.scrollTo(0, 0); },
    toggleGuide(i) { this.openGuideIdx = this.openGuideIdx === i ? -1 : i; },
    setParq(i, val) { this.parqAnswers[i] = val; },
    submitParq() {
      this.route = "HOME";
      if (this.parqAnswers.some(a => a === true)) { this.parqBlocked = true; this.go("centerGuidance"); }
      else { this.parqBlocked = false; this.go("homeGuide"); }
    },
    startCenterRoute() { this.route = "CENTER"; this.go("centerInput"); },
    startProgress() {
      this.progressPct = 0;
      clearInterval(this.progressTimer);
      this.progressTimer = setInterval(() => {
        this.progressPct += 4;
        if (this.progressPct >= 100) {
          this.progressPct = 100;
          clearInterval(this.progressTimer);
          setTimeout(() => this.go("measureResult"), 350);
        }
      }, 45);
    },
    goMeasureProgress() { this.go("measureProgress"); this.$nextTick(() => this.startProgress()); },
  },
  template: `
  <div class="fc-root">
    <div class="fc-phone">
      <div class="fc-topbar">
        <div class="fc-brand"><span class="fc-brand-mark"></span>체력코치 AI</div>
        <span class="fc-step-label">{{ progressLabel }}</span>
      </div>
      <div class="fc-progress-track" v-if="progressPctBar !== null">
        <div class="fc-progress-fill" :style="{ width: progressPctBar + '%' }"></div>
      </div>

      <!-- LANDING -->
      <div class="fc-body" style="display:flex;flex-direction:column;justify-content:center;min-height:640px" v-if="page==='landing'">
        <span class="fc-badge fc-badge-primary">국민체육진흥공단 공공데이터 기반</span>
        <h1 class="fc-h1" style="margin-top:14px;font-size:28px">내 체력을 측정하고<br/>또래와 비교하고<br/>나에게 맞는 운동을 추천받아 보세요.</h1>
        <p class="fc-sub">국민체력100 공식 콘텐츠 기반 AI 체력코치, 체력코치 AI</p>
        <button class="fc-btn fc-btn-primary" @click="go('login')">체력 측정 시작하기</button>
      </div>

      <!-- LOGIN -->
      <div class="fc-body" v-if="page==='login'">
        <button class="fc-nav-back" @click="go('landing')">← 이전</button>
        <span class="fc-badge fc-badge-mock">MOCK — 실제 인증 미연동</span>
        <h1 class="fc-h1" style="margin-top:12px">로그인</h1>
        <p class="fc-sub">이번 MVP는 실제 인증 API가 연결되지 않아 로그인 흐름만 시연합니다.</p>
        <div class="fc-field"><label class="fc-label">아이디</label><input class="fc-input" value="demo_user" readonly /></div>
        <div class="fc-field"><label class="fc-label">비밀번호</label><input class="fc-input" type="password" value="mockpass" readonly /></div>
        <button class="fc-btn fc-btn-primary" @click="go('basicInfo')">Mock으로 로그인</button>
      </div>

      <!-- BASIC INFO -->
      <div class="fc-body" v-if="page==='basicInfo'">
        <button class="fc-nav-back" @click="go('login')">← 이전</button>
        <h1 class="fc-h1">기본정보</h1>
        <p class="fc-sub">체력 비교와 배터리 구성을 위해 최소 정보만 입력해요.</p>
        <div class="fc-field">
          <label class="fc-label">성별</label>
          <div class="fc-select-grid">
            <div :class="['fc-pill', form.gender==='여성' ? 'active':'']" @click="form.gender='여성'">여성</div>
            <div :class="['fc-pill', form.gender==='남성' ? 'active':'']" @click="form.gender='남성'">남성</div>
          </div>
        </div>
        <div class="fc-field"><label class="fc-label">연령(만 나이)</label><input class="fc-input" type="number" placeholder="예: 34" v-model="form.age" /></div>
        <div class="fc-field"><label class="fc-label">신장</label><div class="fc-input-row"><input class="fc-input" type="number" placeholder="170" v-model="form.height" /><span class="fc-unit">cm</span></div></div>
        <div class="fc-field"><label class="fc-label">체중</label><div class="fc-input-row"><input class="fc-input" type="number" placeholder="65" v-model="form.weight" /><span class="fc-unit">kg</span></div></div>
        <button class="fc-btn fc-btn-primary" :disabled="!basicInfoValid" @click="go('routeSelect')">다음</button>
      </div>

      <!-- ROUTE SELECT -->
      <div class="fc-body" v-if="page==='routeSelect'">
        <button class="fc-nav-back" @click="go('basicInfo')">← 이전</button>
        <h1 class="fc-h1">측정 경로 선택</h1>
        <p class="fc-sub">두 경로는 이후 동일한 리포트·추천 파이프라인으로 이어져요.</p>
        <div class="fc-route-card" @click="startCenterRoute">
          <span class="fc-badge fc-badge-good">CENTER</span>
          <h2 class="fc-h2" style="margin-top:10px">센터에서 측정했어요</h2>
          <p class="fc-sub" style="margin-bottom:0">국민체력100 센터의 공식 측정 결과를 입력해요. 근력·심폐지구력 등 전 항목이 포함될 수 있어요.</p>
        </div>
        <div class="fc-route-card" @click="go('parq')">
          <span class="fc-badge fc-badge-warn">HOME</span>
          <h2 class="fc-h2" style="margin-top:10px">집에서 직접 측정할게요</h2>
          <p class="fc-sub" style="margin-bottom:0">안전 문진(PAR-Q) 이후 자가측정을 진행해요. 근력·심폐지구력은 홈 배터리에 포함되지 않아요.</p>
        </div>
      </div>

      <!-- PAR-Q -->
      <div class="fc-body" v-if="page==='parq'">
        <button class="fc-nav-back" @click="go('routeSelect')">← 이전</button>
        <span class="fc-badge fc-badge-good">전신체상태설문지 원문 반영</span>
        <h1 class="fc-h1" style="margin-top:12px">PAR-Q 사전 문진</h1>
        <p class="fc-sub">자가측정 전 안전 확인을 위한 7문항이에요. 하나라도 '예'이면 자가측정 대신 센터 측정을 안내해요.</p>
        <div class="fc-parq-item" v-for="(q,i) in parqQuestions" :key="i">
          <div class="fc-parq-q">{{ i+1 }}. {{ q }}</div>
          <div class="fc-yn">
            <button :class="['no', parqAnswers[i]===false ? 'active':'']" @click="setParq(i,false)">아니오</button>
            <button :class="['yes', parqAnswers[i]===true ? 'active':'']" @click="setParq(i,true)">예</button>
          </div>
        </div>
        <button class="fc-btn fc-btn-primary" :disabled="!parqAnswered" @click="submitParq" style="margin-top:8px">제출하기</button>
      </div>

      <!-- HOME GUIDE -->
      <div class="fc-body" v-if="page==='homeGuide'">
        <button class="fc-nav-back" @click="go('parq')">← 이전</button>
        <h1 class="fc-h1">홈 측정 가이드</h1>
        <p class="fc-sub">{{ ageGroup==='senior' ? '어르신' : '성인' }} 홈 배터리 {{ battery.length }}종이에요. 항목을 눌러 방법을 확인하세요.</p>
        <div class="fc-card" v-for="(it,i) in battery" :key="it.code" @click="toggleGuide(i)" style="cursor:pointer">
          <div class="fc-guide-item-head">
            <h2 class="fc-h2" style="margin-bottom:0">{{ i+1 }}. {{ it.name }}</h2>
            <span>{{ openGuideIdx===i ? '▾' : '▸' }}</span>
          </div>
          <div v-if="openGuideIdx===i" style="margin-top:10px">
            <div class="fc-guide-row"><span class="fc-guide-label">왜</span>{{ it.why }}</div>
            <div class="fc-guide-row"><span class="fc-guide-label">준비물</span>{{ it.prep }}</div>
            <div class="fc-guide-row"><span class="fc-guide-label">공간</span>{{ it.space }}</div>
            <div class="fc-guide-row"><span class="fc-guide-label">방법</span>{{ it.method }}</div>
            <div class="fc-guide-row"><span class="fc-guide-label">주의</span>{{ it.caution }}</div>
            <div class="fc-card-soft" v-if="it.note" style="margin-top:8px;margin-bottom:0">
              <span class="fc-badge fc-badge-primary">측정 오차 핵심 기준</span>
              <p class="fc-sub" style="margin:8px 0 0">{{ it.note }}</p>
            </div>
          </div>
        </div>
        <div class="fc-card-soft">
          <h2 class="fc-h2">악력 (선택 모듈)</h2>
          <p class="fc-sub">악력계가 있으면 근력도 측정할 수 있어요.</p>
          <div class="fc-select-grid">
            <div :class="['fc-pill', gripOwned===true ? 'active':'']" @click="gripOwned=true">악력계 있어요</div>
            <div :class="['fc-pill', gripOwned===false ? 'active':'']" @click="gripOwned=false">없어요</div>
          </div>
        </div>
        <button class="fc-btn fc-btn-primary" :disabled="gripOwned===null" @click="go('measureInput')">측정 시작하기</button>
      </div>

      <!-- MEASURE INPUT (HOME) -->
      <div class="fc-body" v-if="page==='measureInput'">
        <button class="fc-nav-back" @click="go('homeGuide')">← 이전</button>
        <h1 class="fc-h1">측정 결과 입력</h1>
        <span class="fc-badge fc-badge-blocked">정상범위 수치 미확정 · BLOCKED</span>
        <p class="fc-sub" style="margin-top:10px">빈값·음수만 우선 검증해요. 항목별 정상범위 검증은 확정 후 추가돼요.</p>
        <div class="fc-field" v-for="it in homeMeasuredItems" :key="it.code">
          <label class="fc-label">{{ it.name }}</label>
          <div class="fc-input-row">
            <input class="fc-input" type="number" placeholder="0" v-model="homeValues[it.code]" />
            <span class="fc-unit">{{ it.unit }}</span>
          </div>
        </div>
        <button class="fc-btn fc-btn-primary" :disabled="!homeInputAllFilled" @click="goMeasureProgress">입력 완료</button>
      </div>

      <!-- PROGRESS -->
      <div class="fc-body" style="display:flex;flex-direction:column;justify-content:center;align-items:center;min-height:500px;text-align:center" v-if="page==='measureProgress'">
        <div class="fc-progress-circle">{{ progressPct }}%</div>
        <h2 class="fc-h2">결과를 분석하고 있어요</h2>
        <p class="fc-sub">또래 비교 리포트를 준비하는 중이에요.</p>
      </div>

      <!-- MEASURE RESULT -->
      <div class="fc-body" v-if="page==='measureResult'">
        <h1 class="fc-h1">측정 결과 확인</h1>
        <p class="fc-sub">입력한 값을 확인하고 리포트로 이동하세요.</p>
        <div class="fc-card" style="display:flex;justify-content:space-between" v-for="it in homeMeasuredItems" :key="it.code">
          <span style="font-weight:600">{{ it.name }}</span>
          <span style="font-family:var(--mono)">{{ homeValues[it.code] }}{{ it.unit }}</span>
        </div>
        <button class="fc-btn fc-btn-primary" @click="go('report')">리포트 보기</button>
      </div>

      <!-- CENTER INPUT -->
      <div class="fc-body" v-if="page==='centerInput'">
        <button class="fc-nav-back" @click="go('routeSelect')">← 이전</button>
        <span class="fc-badge fc-badge-good">CENTER</span>
        <h1 class="fc-h1" style="margin-top:10px">센터 측정 결과 입력</h1>
        <p class="fc-sub">국민체력100 센터에서 받은 측정 결과를 그대로 입력해요.</p>
        <div class="fc-field" v-for="it in centerMeasuredItems" :key="it.code">
          <label class="fc-label">{{ it.name }}</label>
          <div class="fc-input-row">
            <input class="fc-input" type="number" placeholder="0" v-model="centerValues[it.code]" />
            <span class="fc-unit">{{ it.unit }}</span>
          </div>
        </div>
        <button class="fc-btn fc-btn-primary" :disabled="!centerInputAllFilled" @click="go('report')">리포트 보기</button>
      </div>

      <!-- CENTER GUIDANCE -->
      <div class="fc-body" v-if="page==='centerGuidance'">
        <h1 class="fc-h1">체력인증센터 안내</h1>
        <div class="fc-card-soft" v-if="parqBlocked">
          <span class="fc-badge fc-badge-blocked">PAR-Q 1개 이상 '예'</span>
          <p class="fc-sub" style="margin:10px 0 0">서비스 이용 차단이 아니라, 안전한 측정 경로로 안내해 드려요.</p>
        </div>
        <div class="fc-card">
          <h2 class="fc-h2">지금 이용 가능해요</h2>
          <button class="fc-btn fc-btn-outline" style="margin-bottom:8px" @click="go('centerInput')">센터 측정 결과 입력</button>
          <button class="fc-btn fc-btn-outline" style="margin-bottom:8px" @click="go('video')">공단 운동 영상 열람</button>
          <button class="fc-btn fc-btn-outline" @click="window.open('https://nfa.kspo.or.kr','_blank')">가까운 체력인증센터 찾기</button>
        </div>
        <div class="fc-card">
          <h2 class="fc-h2">지금은 잠겨 있어요</h2>
          <div class="fc-locked-row">🔒 자가측정</div>
          <div class="fc-locked-row">🔒 자동 운동처방</div>
          <div class="fc-locked-row">🔒 주간 루틴</div>
        </div>
        <p class="fc-disclaimer">본 리포트는 자가측정 기반 참고 정보이며, 국민체력100 공식 인증등급이 아닙니다. 의학적 진단을 대체하지 않습니다.</p>
      </div>

      <!-- REPORT -->
      <div class="fc-body" v-if="page==='report'">
        <h1 class="fc-h1">나의 체력 리포트</h1>
        <span class="fc-badge fc-badge-mock">{{ normPeriodNote }}</span>

        <div class="fc-section-divider"></div>
        <h2 class="fc-h2">① 나의 측정 결과
          <span :class="['fc-trust-badge', route==='CENTER' ? 'fc-trust-center':'fc-trust-home']">{{ route==='CENTER' ? '센터 측정' : '자가측정 기준' }}</span>
        </h2>
        <div class="fc-card" style="display:flex;justify-content:space-between" v-for="it in reportItems" :key="it.code">
          <span style="font-weight:600">{{ it.name }}</span>
          <span style="font-family:var(--mono)">{{ reportValues[it.code] || '—' }}{{ it.unit }}</span>
        </div>

        <div class="fc-section-divider"></div>
        <h2 class="fc-h2">② 또래 비교</h2>
        <div class="fc-range-row" v-for="row in comparisonRows" :key="row.code">
          <div class="fc-range-head"><span class="fc-range-name">{{ row.name }}</span><span class="fc-range-value">{{ row.value }}{{ row.unit }}</span></div>
          <div class="fc-range-track">
            <div class="fc-range-fill" v-if="row.range" :style="{ left: row.range[0]+'%', width: (row.range[1]-row.range[0])+'%' }"></div>
          </div>
          <div class="fc-range-caption">{{ row.text }}</div>
        </div>
        <p class="fc-range-caption" v-if="route==='CENTER'">CENTER 결과는 구간이 아닌 단일 값으로 제공돼요(MOCK).</p>

        <div class="fc-section-divider"></div>
        <h2 class="fc-h2">③ 강점 / 약점</h2>
        <div class="fc-card"><span class="fc-badge fc-badge-good">강점</span> {{ strongest && strongest.name }}</div>
        <div class="fc-card"><span class="fc-badge fc-badge-warn">약점</span> {{ weakest && weakest.name }}</div>

        <template v-if="unmeasuredList.length">
          <div class="fc-section-divider"></div>
          <h2 class="fc-h2">④ 아직 측정하지 않은 항목</h2>
          <div class="fc-unmeasured" v-for="u in unmeasuredList" :key="u.label">
            <strong>{{ u.label }}</strong>
            <p class="fc-sub" style="margin:4px 0 0">{{ u.note }}</p>
          </div>
        </template>

        <div class="fc-section-divider"></div>
        <h2 class="fc-h2">⑤ 나의 운동 추천</h2>
        <p class="fc-sub">{{ weakest && weakest.name }} 결과를 바탕으로 한 보완 루틴을 준비했어요.</p>
        <button class="fc-btn fc-btn-primary" @click="go('recommend')">운동 추천 보기</button>

        <div class="fc-section-divider"></div>
        <h2 class="fc-h2">⑥ 센터 측정 안내</h2>
        <button class="fc-btn fc-btn-outline" @click="go('centerGuidance')">가까운 체력인증센터 알아보기</button>

        <p class="fc-disclaimer">본 리포트는 자가측정 기반 참고 정보이며, 국민체력100 공식 인증등급이 아닙니다. 의학적 진단을 대체하지 않습니다.</p>
      </div>

      <!-- RECOMMEND -->
      <div class="fc-body" v-if="page==='recommend'">
        <button class="fc-nav-back" @click="go('report')">← 이전</button>
        <h1 class="fc-h1">오늘의 운동</h1>
        <span class="fc-badge fc-badge-mock">MOCK DATA — 실제 처방 콘텐츠 연결 전</span>
        <div class="fc-section-divider"></div>
        <div class="fc-card">
          <span class="fc-badge fc-badge-primary">기본 구성</span>
          <h2 class="fc-h2" style="margin-top:8px">가벼운 유산소 걷기 10분</h2>
        </div>
        <div class="fc-card">
          <span class="fc-badge fc-badge-primary">기본 구성</span>
          <h2 class="fc-h2" style="margin-top:8px">코어 안정화 플랭크 3세트</h2>
        </div>
        <div class="fc-card">
          <span class="fc-badge fc-badge-warn">약점 가중</span>
          <h2 class="fc-h2" style="margin-top:8px">{{ weakestHomeName || '약점 요인' }} 보완 스트레칭</h2>
          <p class="fc-sub" style="margin-bottom:12px">{{ weakestHomeName }} 결과를 바탕으로 추천돼요.</p>
          <button class="fc-btn fc-btn-outline" @click="go('video')">운동 영상 보기</button>
        </div>
        <p class="fc-sub" style="margin-top:4px">측정하지 않은 요인이 있어도 기본 루틴의 유산소·근력 요소는 유지돼요.</p>
      </div>

      <!-- VIDEO -->
      <div class="fc-body" v-if="page==='video'">
        <button class="fc-nav-back" @click="go('recommend')">← 이전</button>
        <h1 class="fc-h1">국민체력100 운동 영상</h1>
        <span class="fc-badge fc-badge-mock">MOCK — 실제 영상 콘텐츠 미연결</span>
        <div class="fc-section-divider"></div>
        <div class="fc-video-card" v-for="v in ['유연성 스트레칭 기초','하체 순발력 향상 루틴','코어 안정화 운동','제자리걷기 유산소 루틴']" :key="v">
          <div class="fc-video-thumb">▶</div>
          <div><div style="font-weight:700;font-size:14px">{{ v }}</div><div class="fc-sub" style="margin:2px 0 0">국민체력100 공식 콘텐츠</div></div>
        </div>
      </div>

    </div>
  </div>
  `,
};

const app = createApp(App);
app.mount("#app");
