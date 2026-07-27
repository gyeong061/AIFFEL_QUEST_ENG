# AIFFEL Campus Online Code Peer Review Templete
- 코더 : 김수경
- 리뷰어 : 조희연


# PRT(Peer Review Template)
- [x]  **1. 주어진 문제를 해결하는 완성된 코드가 제출되었나요?**
    - 문제에서 요구하는 최종 결과물이 첨부되었는지 확인
        - 세 가지 평가기준(① 데이터 정제 + Generation 기법 실험, ② SFT vs RM/RLHF 비교, ③ Base KoGPT-2 vs SFT 비교)을 모두 충족하는 `Base → SFT → RM → RLHF(PPO)` 전체 파이프라인이 하나의 노트북(`KoChatGPT_프로젝트.ipynb`)에 완성되어 제출되었습니다.
        - 근거: 데이터 EDA(섹션 1) → 정제(섹션 2) → Base 생성(섹션 3) → LoRA SFT(섹션 4) → Generation 실험(섹션 5) → RM 학습·검증(섹션 6) → PPO(섹션 7) → BLEU/ROUGE 정량 평가(섹션 8) → 정성 비교표(섹션 9)까지 각 셀의 출력이 정상적으로 남아 있어 실행 완결성이 확인됩니다.

- [x]  **2. 전체 코드에서 가장 핵심적이거나 가장 복잡하고 이해하기 어려운 부분에 작성된
주석 또는 doc string을 보고 해당 코드가 잘 이해되었나요?**
    - 가장 핵심적이라고 본 부분: **섹션 4의 `SFT_dataset` 클래스**입니다. Instruction-Response 프롬프트 포맷을 만들고, source 길이만큼 label을 `-100`으로 마스킹하여 응답 토큰에 대해서만 loss가 계산되도록 하는 부분이 SFT 학습 품질을 좌우하는 가장 이해가 까다로운 로직입니다.
        ```python
        input_ids = examples_tokenized["input_ids"]
        labels = copy.deepcopy(input_ids)
        for label, source_len in zip(labels, sources_tokenized["input_ids_lens"]):
            label[:source_len] = -100   # prompt 구간은 loss에서 제외 → 응답 학습에 집중
        ```
    - LoRA 적용부(섹션 4)의 `# 파라미터가 얼마나 줄었는지 확인용` 주석, `PROMPT_DICT` 포맷 정의 등이 함께 있어 각 블록의 존재 이유가 잘 드러났고, 특히 섹션 6 RM과 섹션 8 BLEU/ROUGE의 markdown 설명이 코드의 의도를 명확히 이해하는 데 큰 도움이 되었습니다.

- [x]  **3. 에러가 난 부분을 디버깅하여 문제를 해결한 기록을 남겼거나
새로운 시도 또는 추가 실험을 수행해봤나요?**
    - 디버깅 기록: 섹션 7 PPO 저장 시 발생한 `AttributeError`(GPTActor 래퍼에는 `save_pretrained`가 없음)의 원인을 markdown으로 분석하고, `actor.model.save_pretrained(...)`로 내부 HF 모델을 저장하는 해결책을 별도 셀로 남겼습니다.
    - 추가 실험: ① 원본 SFT vs 정제 SFT를 분리 학습해 데이터 정제 효과를 정량 비교, ② Greedy/Beam/Top-k·Top-p/Repetition Penalty 등 다양한 Generation 기법 비교(섹션 5), ③ **보상 해킹(Reward Hacking)** 현상을 직접 관측하고 원인(RM 점수만 높이는 형식 모방)을 분석한 점이 특히 인상적이었습니다.

- [x]  **4. 회고를 잘 작성했나요?**
    - 섹션 9 종합 비교 분석과 "핵심 인사이트", "프로젝트 회고(Keep/Problem/Try)"에 배운 점·아쉬운 점·향후 개선 방향(KL 페널티 튜닝, 더 큰 Foundation Model, BERTScore/LLM-as-a-Judge 도입)이 구체적으로 정리되어 있습니다.
    - 정성 평가를 관련성/유창성/완결성/정보성 4개 항목의 표로 만들어 모델 간 차이를 정리한 점이 이해를 크게 돕습니다.
    - (제안) 텍스트로는 파이프라인 단계가 잘 정리되어 있으나, `Base → SFT → RM → PPO → 평가`의 전체 실행 플로우를 다이어그램(그래프) 이미지로 한 장 넣어주면 흐름 파악이 더 직관적일 것 같습니다.

- [x]  **5. 코드가 간결하고 효율적인가요?**
    - `clean_text`, `is_valid_*`, `refine_*` 등 데이터 정제 로직을 목적별 함수로 분리하고, `compute_bleu`/`compute_rouge`/`evaluate_responses`로 평가 로직을 모듈화하여 중복을 최소화했습니다.
    - LoRA(`r=16`, `alpha=32`)로 학습 파라미터 수를 줄이고, 셀 종료 시 `del model; torch.cuda.empty_cache()`로 T4 GPU 메모리를 관리한 점이 효율적입니다.
    - (사소한 제안) `compute_bleu`의 `except: return 0.0`는 예외 타입을 명시(`except Exception`)하면 PEP8·디버깅 측면에서 더 좋고, BLEU/ROUGE 토크나이즈가 공백 분할 기반이라 한국어에서는 형태소 단위 토크나이즈를 쓰면 점수가 더 신뢰도 있을 것 같습니다.


# 회고(참고 링크 및 코드 개선)
```
- 세 가지 평가기준을 모두 만족하는 RLHF 전체 파이프라인을 하나의 노트북에서 실행까지 완결한 점이 인상적이었습니다.
  특히 "SFT는 정답을 외워 BLEU/ROUGE가 인위적으로 높아진다(암기 함정)"는 점과, PPO 이후 RM 점수는 올랐지만
  실제 텍스트 품질은 무너지는 '보상 해킹'을 직접 관측·분석해낸 부분에서 많이 배웠습니다.

- 개선 제안
  1) 실행 플로우 다이어그램(Base→SFT→RM→PPO→평가) 이미지 1장 추가 → 회고 항목 4 완성도 상승
  2) compute_bleu 의 bare except → except Exception 으로 명시 (PEP8)
  3) 한국어 BLEU/ROUGE는 공백 분할 대신 형태소 토크나이저(예: Kiwi/Mecab) 기반으로 계산하면 지표 신뢰도 향상
  4) 보상 해킹 완화를 위해 PPO 의 KL penalty(kl_coef) 값을 명시적으로 로깅/튜닝해보면 좋겠습니다.

- 참고 링크
  - HuggingFace PEFT(LoRA): https://huggingface.co/docs/peft
  - RLHF & Reward Hacking 개요: https://huggingface.co/blog/rlhf
```
