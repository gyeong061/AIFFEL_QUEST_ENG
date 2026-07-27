# AIFFEL Campus Online Code Peer Review Templete
- 코더 : gyeong061
- 리뷰어 : (리뷰어 이름)

# PRT(Peer Review Template)

- [x]  **1. 주어진 문제를 해결하는 완성된 코드가 제출되었나요?**
    - 59셀 전체가 실행된 상태이고, TODO 3종(RRF 구현, Self-RAG 프롬프트, KLUE-MRC 추가 실습)이 모두 채워져 있습니다.
    - KorQuAD (셀 29): context_precision 0.733→0.800, faithfulness 0.750→0.804
    - KLUE-MRC (셀 53): **context_precision 0.642→0.892 (+0.250)**, answer_relevancy 0.252→0.293
    - 헤더의 "Multi-Query → RAG-Fusion → HyDE → Reranking → Self-RAG" 순서가 셀 21 `advanced_retrieve` 안에서 실제 호출 순서로 이어져 있습니다.

- [x]  **2. 핵심적이거나 복잡한 부분의 주석/docstring을 보고 코드가 잘 이해되었나요?**
    - 셀 15 `reciprocal_rank_fusion` — `# 같은 본문은 같은 문서로 간주해 여러 쿼리의 점수를 누적합니다.` RRF에서 제일 자주 틀리는 문서 동일성 기준을 `page_content`로 잡은 이유가 바로 위에 있어 이해됐습니다.
    - 셀 23 `self_rag` — `# NO가 명확할 때만 검색을 건너뜁니다. 형식이 깨지면 안전하게 검색합니다.` fail-safe 방향을 명시했고 `startswith("NO")`로 동작도 일치합니다.

- [x]  **3. 디버깅 기록을 남겼거나 새로운 시도/추가 실험을 했나요?**
    - 디버깅: 셀 4에서 uninstall → 버전 핀 고정 2단계로 나누고 `pip resolver 백트래킹 방지` 이유를 명시. 셀 39는 300k 토큰/요청 한도를 피해 100개씩 배치 적재.
    - 추가 실험: ① 원본이 지시문만 주고 비워둔 KLUE-MRC 실습 전체 구현(뉴스 문체용 프롬프트 포함) ② 선택 과제였던 paired t-test 수행(셀 56) ③ 요구에 없던 두 도메인 통합 비교표 `compare_domains`.

- [x]  **4. 회고를 잘 작성했나요?**
    - 셀 58이 검색 강화 / Self-RAG / RAGAS / 도메인 특성 4축으로 정리되어 있고, `answer_relevancy`가 낮은 것을 모델 탓이 아니라 "정답이 한 단어라 역추론이 흐려진다"는 데이터셋 구조로 짚은 것이 정확합니다.
    - 아쉬운 점 1) t-test 결론이 회고에 없습니다. Δ는 양수인데 검정은 4개 지표 모두 p > 0.05(차이 없음)였고, 이 충돌이 핵심 배움입니다.
    - 아쉬운 점 2) 셀 57 Quiz의 대괄호가 안 채워졌습니다. 실행값은 1번 **`faithfulness` (-0.151)**, 2번 **`context_precision` (+0.250)** 입니다.

- [x]  **5. 코드가 간결하고 효율적인가요?**
    - collection 이름을 `"korquad_v1"` / `"klue_mrc"`로 분리해 두 벤치마크가 섞이지 않게 한 것이 가장 중요한 위생 처리입니다. 2GB reranker도 `reranker_klue = reranker`로 재사용했습니다.
    - 개선 제안:
      1. **`metrics` 변수 shadowing (셀 56)** — 셀 28의 RAGAS 지표 객체를 문자열 리스트로 덮어써서, 셀 56 실행 후 셀 53을 다시 돌리면 깨집니다. `metric_names`로 이름만 바꾸면 됩니다.
      2. t-test가 KorQuAD만 검정합니다. 정작 유의할 가능성이 있는 KLUE `context_precision`(Δ+0.250)이 빠졌습니다.
      3. `advanced_retrieve`/`_klue`, `self_rag`/`_klue`가 db·프롬프트·hyde 3개만 다르고 로직은 같습니다(약 70줄 중복). 파라미터화하면 한쪽만 고쳐 결과가 어긋나는 사고를 막습니다.

# 회고(참고 링크 및 코드 개선)

```
[리뷰어 회고]
RRF의 문서 동일성 판정을 배웠습니다. 저는 Document를 dict 키로 쓰려다 unhashable
에러를 만나 id()로 우회했고, 같은 청크가 중복 집계되는 걸 뒤늦게 발견했습니다.

Self-RAG의 fail-safe 방향도 배웠습니다. 저는 startswith("YES")로 검사해서 형식이
깨지면 검색을 건너뛰는 쪽으로 무너졌는데, 이 노트북은 반대로 잡아뒀습니다.
판정 실패 시 어느 쪽이 덜 위험한지 먼저 정하고 조건문을 쓴다는 게 핵심 같습니다.

[참고 링크]
- Reciprocal Rank Fusion (Cormack et al., 2009) — k=60 관례의 출처
  https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf
- HyDE (Gao et al., 2022) https://arxiv.org/abs/2212.10496
- Self-RAG (Asai et al., 2023) https://arxiv.org/abs/2310.11511

[개선 제안 코드] t-test를 두 도메인에 모두 적용 + metrics shadowing 제거
```
