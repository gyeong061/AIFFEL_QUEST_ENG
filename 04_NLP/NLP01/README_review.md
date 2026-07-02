# AIFFEL Campus Online Code Peer Review Template
- 코더 : 정슬기
- 리뷰어 : 김수경

---

# PRT(Peer Review Template)

- [x] **1. 주어진 문제를 해결하는 완성된 코드가 제출되었나요?**

    **✅ 충족**

    한국어 → 영어 번역기를 목표로 한 Seq2Seq with Attention 모델이 전체 파이프라인으로 완성되었습니다.

    완성된 구성 요소:
    - 데이터 로드 및 중복 제거 (Cell 9~11)
    - 전처리 함수 `preprocess_kor`, `preprocess_eng` (Cell 13)
    - Mecab + SentencePiece 토큰화 (Cell 15, 20)
    - `TranslationDataset`, `DataLoader` (Cell 21, 23)
    - `Encoder`, `BahdanauAttention`, `Decoder`, `Seq2Seq` 클래스 (Cell 25)
    - 학습 루프 + Early Stopping + ReduceLROnPlateau (Cell 29~31)
    - 번역 테스트 함수 `translate_korean` (Cell 33)
    - 어텐션 시각화 `translate_with_attention` (Cell 37)
    - 최종 Test Loss 평가 (Cell 34)

    최적 하이퍼파라미터 조합 기록 (Cell 39):
    ```
    EMB 256, HIDDEN 512, dropout 0.5
    NUM_SAMPLES = len(cleaned_corpus)
    weight_decay = 1e-4, LR = 1e-3
    → "현재 이 조합이 가장 좋은 결과"
    ```

---

- [x] **2. 전체 코드에서 가장 핵심적이거나 가장 복잡하고 이해하기 어려운 부분에 작성된 주석 또는 doc string을 보고 해당 코드가 잘 이해되었나요?**

    **✅ 부분 충족**

    잘 작성된 부분:

    전처리 함수에 doc string이 명확하게 달려 있습니다 (Cell 13):
    ```python
    def preprocess_kor(text):
        """한국어 전처리: 한글 + 영문 + 숫자 + 기본 구두점만 남김"""

    def preprocess_eng(text):
        """영어 전처리 + <start>/<end> 토큰 추가"""
    ```

    학습 루프에서 핵심 개념 주석이 달려 있습니다 (Cell 29):
    ```python
    # tgt = [<start>, w1, w2, ..., <end>] → 한 칸 어긋난 입력/라벨
    tgt_input = tgt[:, :-1]
    tgt_label = tgt[:, 1:]
    ```

    아쉬운 부분:
    - `BahdanauAttention`, `Decoder`, `Seq2Seq` 클래스 내부에는 주석이 부족합니다.
    - `translate_with_attention` 함수 내 Decoder step-by-step 부분에 주석이 더 있었으면 좋겠습니다. ( 개인적인의견.....)

---

- [x] **3. 에러가 난 부분을 디버깅하여 문제를 해결한 기록을 남겼거나 새로운 시도 또는 추가 실험을 수행해봤나요?**

    **✅ 충족**

    디버깅 및 추가 시도 기록 (Cell 41):
    > "처음에는 단어 단위 토크나이저(kor_tokenizer)로 시작했다가 나중에 SentencePiece(kor_sp)로 전환했는데, 가장 최근에 배운 부분을 놓쳐서 코드 작성에 부족함이 많다는걸 배우는 시간이었다."

    추가 실험 기록:
    - EMB_DIM / HIDDEN_DIM 값을 바꿔가며 성능 비교 (128/256/512 조합 실험)
    - Early Stopping (patience=3) 적용
    - ReduceLROnPlateau 스케줄러 추가 (factor=0.5, patience=2)
    - L2 정칙화 weight_decay 실험 (1e-5 → 1e-4로 조정)
    - Dropout 0.5 추가로 과적합 방지 시도
    - NUM_SAMPLES를 30,000 → 전체 데이터로 확장

    데이터 분할을 Train 70% / Valid 15% / Test 15%로 세분화한 것도 기본 80/20 대비 개선된 시도입니다 (Cell 23).

---

- [x] **4. 회고를 잘 작성했나요?**

    **✅ 충족**

    Cell 39~41에 걸쳐 배운 점, 아쉬운 점, 느낀 점이 상세히 기록되어 있습니다.

    배운 점 (Cell 41):
    > "GRU+Attention은 2014년 수준 아키텍처로 한-영처럼 어순이 다른 언어쌍에서는 한계가 명확하며, 94k 데이터는 NMT 기준 매우 적은 양. 이를 통해 '모델 선택 자체가 가장 큰 결정'임을 체감"

    아쉬운 점 (Cell 40):
    > "마지막 최종 수정 과정에서 Bidirectional Encoder를 놓쳤다는 걸 알았다"
    > "Epoch이나 batch_size를 조금 포기하더라도 더 테스트를 해봤어야 하는 생각도 든다"

    느낀 점:
    > "하이퍼파라미터를 조절하면서 다양한 결과값을 비교하고 다양한 성능 테스트를 하면서 많이 배웠다"

    아쉬운 부분:
    - 코드 실행 플로우를 그래프(다이어그램)로 시각화한 부분이 없어서, 흐름을 한눈에 파악하기가 어렵습니다.( 제 수준이 이정도라;)
    - 단, 코드자체의 주석이나 설계가 깔끔해서 충분히 인지할 수 있었습니다.

---

- [x] **5. 코드가 간결하고 효율적인가요?**

    **✅ 부분 충족**

    잘 된 부분:
    - `preprocess_kor`, `preprocess_eng`, `tokenize_kor`, `tokenize_eng`를 함수로 분리하여 재사용성을 높였습니다.
    - `train_one_epoch`, `evaluate`를 별도 함수로 분리해 학습 루프가 깔끔합니다.
    - `SEED`, `MAX_LEN`, `BATCH_SIZE`, `VOCAB_SIZE` 등 상수를 상단에 모아 관리합니다.
    - `@torch.no_grad()` 데코레이터를 평가 함수에 적용해 메모리 효율을 높였습니다.
    - `tqdm`으로 진행 상황을 시각적으로 표시합니다.

    개선 여지: (클로드 의견참고)
    - `import os`가 Cell 5와 Cell 8에 중복 import 됩니다.
    - `BahdanauAttention`의 변수명이 원본 노트북(NLP01)과 달리 `W_enc`, `W_dec`로 바뀌어 있어 일관성은 좋으나, 이 변경 이유에 대한 주석이 있었으면 더 좋았을 것 같습니다.
    - `Bidirectional Encoder`가 미구현 상태로 남아 있어, 코드의 완성도 측면에서 아쉬움이 있습니다.

---

# 회고(참고 링크 및 코드 개선)

```
## 종합 의견

이번 과제는 Seq2Seq with Attention 구조를 처음부터 직접 구현하고,
하이퍼파라미터를 반복 실험하며 최적 조합을 찾아낸 과정이 인상적이었습니다.

특히 아래 세 가지 시도가 돋보였습니다:
1. 단순 80/20 분할 대신 Train/Valid/Test 70/15/15 분할로 평가를 세분화한 것
2. ReduceLROnPlateau + Early Stopping 조합으로 학습 안정성을 높인 것
3. 모델/데이터의 본질적 한계(GRU+Attention의 구조적 한계, 데이터 양)를
   스스로 인식하고 회고에 명확히 기록한 것

직접 코드를 돌리는 작업을 보았을떄, 나는 시도하지못한 , 병렬형식의 학습을 진행하는 걸 보고 매우 인상적 이었습니다.
노트북의 성능에따라 속도는 다를 수 있지만, 시도해보지 못한것과 안한것이 차이가 클 수 있다는 걸 깨달았습니다.
간결하고 정리된 코드 형식이라 , 좀더 분석하기 편했다.

