✅ Chapter 13 체크포인트

1. ML 테스트가 "다크 소울"이라 불리는 이유를 전통 소프트웨어와 비교하여 3가지 관점에서 설명할 수 있으신가요?
- 판단 기준의 차이 (부분적 실패): 전통 소프트웨어는 테스트 통과 여부가 명확(맞다/틀리다)하지만, ML 모델은 0이 아닌 손실(Non-zero loss)을 가지며 항상 어느 정도 틀려 있습니다. 따라서 값이 정확히 일치하는지가 아니라 "얼마나 틀리느냐가 허용 범위 내에 있는지"를 판단해야 합니다.

- 확률적(Probabilistic) 특성: 전통 소프트웨어는 동일 입력에 동일 출력이 보장되는 결정론적 시스템이지만, ML 모델은 데이터 셔플링이나 부동 소수점 오차 등에 의해 결과가 미세하게 달라지는 확률적 시스템입니다.

- 조용한 실패(Silent Failure): 코드가 잘못되면 프로그램이 죽지만, ML에서 데이터가 잘못되면 에러 발생 없이 모델이 조용히 잘못된 패턴을 학습하므로 문제를 감지하기가 훨씬 어렵습니다.

2. 테스트 수트를 "분류기"로 보았을 때, 오탐(False Alarm)이 왜 위험한지 실제 사례를 들어 설명할 수 있으신가요?
:오탐이 많아지면 정상적인 코드 변경에도 테스트가 계속 실패(Fail)를 출력하게 됩니다.

- 위험성(실제 사례): 잦은 오탐에 지친 개발자가 코드의 버그를 찾는 대신, 단순히 알림을 없애기 위해 "테스트 코드 자체를 수정하여 강제로 통과"시키는 상황이 발생합니다. 이는 시스템의 위험을 관리하는 테스트 본연의 가치를 완전히 무너뜨립니다.

3. 암기 테스트(overfit_batches=1)가 실패했을 때 의심해야 할 원인 5가지를 나열하고, 각각의 디버깅 방법을 떠올릴 수 있으신가요?
- 그래디언트 계산 오류: .requires_grad가 False로 설정되었거나 연산 그래프가 단절되지 않았는지 파라미터 연결 상태를 점검합니다.

- 데이터 셔플링 오류: DataLoader에서 입력 데이터(x)와 정답 레이블(y)의 순서가 뒤섞이지 않았는지 확인합니다.

- 전처리 버그: 정규화 과정 등에서 식을 잘못 적용(예: 평균을 빼야 하는데 더함)하지 않았는지 연산 로직을 검토합니다.

- 수치적 문제: 그래디언트 폭주나 소실로 인한 NaN/Inf 값이 발생하는지 모니터링하고 그래디언트 클리핑을 적용합니다.

- 옵티마이저 설정 오류: 학습률이 0으로 설정되었거나 엉뚱한 파라미터 그룹이 전달되지 않았는지 옵티마이저 초기화 코드를 확인합니다.

4. 데이터 기댓값 테스트에서 "느슨한 경계" 원칙이 왜 중요한지, 경계를 너무 엄격하게 잡으면 어떤 문제가 발생하는지 설명해 보세요.
:경계를 너무 엄격하게(예: 사람 키 4~8피트) 설정하면, 정상적인 데이터 변동임에도 불구하고 테스트가 실패하는 불필요한 오탐(False Alarm)이 빈번하게 발생합니다. 반면 경계를 느슨하게(예: 0~30피트) 설정하면, 인치를 피트로 잘못 입력하는 것과 같은 "실제 치명적인 오류(불이 난 상황)"만을 효과적으로 잡아낼 수 있습니다.

5. 행동 테스트의 "불변성 테스트"와 "방향성 테스트"의 차이를 자신의 프로젝트에 적용하여 각각 1개씩 예시를 만들어 보실 수 있나요?
- 불변성 테스트 (Invariance Test): 입력을 변형하더라도 모델의 예측 결과가 동일하게 유지되어야 하는 특성을 검증합니다.

	- 스팸 메일 분류기 예시: "할인 혜택 안내입니다"를 "할인 혜택 안내해 드립니다"로 조사나 어미만 변경했을 때, 두 문장의 스팸 예측 확률이 동일하게 유지되는지 확인합니다.

- 방향성 테스트 (Directional Test): 입력을 특정 의도를 가지고 변경했을 때, 예측 결과도 그에 맞는 명확한 방향으로 변하는지 검증합니다.

	- 스팸 메일 분류기 예시: "할인 혜택 안내입니다"라는 문장 뒤에 "즉시 계좌로 송금 요망"이라는 문구를 추가했을 때, 스팸으로 예측될 확률이 기존보다 확연히 높아지는지 확인합니다.




✅ Chapter 14 체크포인트

1. "Make it Run → Make it Fast → Make it Right" 순서에서, 왜 ML에서는 "Fast"가 "Right"보다 먼저 와야 하는지 설명할 수 있으신가요?
: ML 모델은 본질적으로 확률적이어서 완벽히 올바른("Right") 상태에 도달하는 것은 끝이 없는 과정입니다. 성능을 개선하려면 필연적으로 수많은 실험과 튜닝을 반복해야 하므로, 하루에 여러 번 테스트할 수 있는 빠른 실험 주기("Fast")를 먼저 확보해두지 않으면 성능 개선("Right") 작업 자체가 비효율적이거나 불가능해지기 때문입니다.


2. OOM 오류를 해결하는 4단계 전략을 순서대로 말할 수 있으신가요? Adam이 파라미터의 3~4배 메모리를 쓰는 이유는 무엇인가요?
- 해결 4단계:

	- 정밀도 낮추기 (예: precision="16-mixed")

	- 배치 사이즈 줄이기

	- 그래디언트 축적 (Gradient Accumulation) 적용

	- 그래디언트 체크포인팅 적용 (연산 속도를 약간 희생해 메모리 확보)

- Adam 옵티마이저의 메모리 점유 이유 : Adam은 파라미터를 업데이트할 때 각 파라미터에 대한 1차 모멘텀(평균)과 2차 모멘텀(분산) 상태 값을 모두 저장해야 합니다. 이로 인해 순수 모델 파라미터 크기보다 보통 3~4배 더 많은 메모리를 차지하게 됩니다.


3. 프로파일링 결과에서 `get_train_batch`가 전체 시간의 60%를 차지한다면, 어떤 최적화를 우선 시도하시겠어요? 반대로 `training_step`이 90%라면요?
- get_train_batch가 60% (데이터 굶주림 상태): GPU 연산 속도보다 CPU의 데이터 로딩이 느린 병목 상태입니다. num_workers 증가, persistent_workers=True, pin_memory=True 설정, NVMe SSD로 데이터 배치, GPU 기반 전처리(NVIDIA DALI) 등을 우선 시도해야 합니다.

- training_step이 90% (연산 병목 상태): 모델 연산 자체가 가장 무거운 상태입니다. 혼합 정밀도(16-mixed) 적용, torch.compile을 통한 커널 퓨전, 모델 경량화 등 연산 부하를 줄이는 최적화를 시도해야 합니다.


4. 스케일링 법칙의 "작은 실험 → 직선 외삽 → 필요 자원 추산" 흐름을 자신의 언어로 설명하고, 이것이 비즈니스적으로 어떤 가치를 주는지 설명해 보세요.
- 흐름 설명: 파라미터나 데이터 크기를 점진적으로 늘려가며 3~5개의 작은 실험을 진행하고 각각의 Loss를 기록합니다. 이 점들을 로그-로그 차트에 찍어 직선을 그린 후 연장(외삽)하여, 목표로 하는 성능(Loss)에 도달하기 위해 필요한 자원(데이터 양, GPU 시간)을 정확한 수치로 추산해냅니다.

- 비즈니스적 가치: 엔지니어의 직감이 아닌 수학적 데이터에 기반해 의사결정을 내릴 수 있습니다. "자원을 10배 투입하면 성능이 얼마나 오를까?"라는 질문에 구체적으로 답할 수 있어, 무의미한 실험에 들어가는 비용을 방지하고 목표 성능 달성을 위한 예산을 정확히 추산할 수 있습니다.


5. 성능 저하 진단표(오버피팅/언더피팅/분포 변화)에서, 자신의 최근 프로젝트가 어떤 상황이었는지 분석하고 적절한 처방을 매칭해 보세요.
- 언더피팅 상황 (Train Loss와 Val Loss가 모두 높음):

분석: 모델이 데이터의 복잡한 패턴을 다 학습하지 못한 상태입니다.

처방: 모델의 크기/깊이를 늘리거나(용량 증가), 더 의미 있는 변수를 추가(피처 엔지니어링)합니다.

- 오버피팅 상황 (Train Loss는 낮으나 Val Loss가 높음):

분석: 훈련 데이터의 지엽적인 노이즈까지 지나치게 암기한 상태입니다.

처방: 드롭아웃(Dropout) 등 규제를 추가하거나, 데이터 증강(Augmentation) 기법을 사용해 훈련 데이터를 확장합니다.

- 데이터 드리프트/분포 변화 (Train/Val Loss는 낮으나 실제 서비스 성능이 낮음):

분석: 학습 환경의 데이터와 실제 배포 환경의 데이터 특성이 달라진 상태입니다.

처방: 최신 운영 환경의 데이터를 훈련 및 검증 세트에 추가하여 모델이 바뀐 분포를 학습하게 만듭니다.




✅ Chapter 15 체크포인트

1. LLM 기반 시스템을 Accuracy만으로 평가할 수 없는 이유를 설명하고, 추가로 필요한 평가 차원을 5가지 나열할 수 있으신가요?
- 이유: LLM이 생성하는 답변은 단순히 '맞다/틀리다'의 단일 숫자로 요약할 수 없습니다. "정확하지만 딱딱한 답변"과 "자연스럽지만 환각이 섞인 답변" 중 어떤 것이 나은지는 비즈니스 맥락에 따라 다르며, 단일 지표로는 모델의 구체적인 약점을 파악할 수 없기 때문입니다.

- 5가지 평가 차원:

1. 유창성 (Fluency): 답변이 자연스럽게 읽히는가

2. 사실성 (Faithfulness): 환각(Hallucination) 없이 사실에 기반하는가

3. 스타일 (Tone): 톤과 매너가 적절한가

4. 출처 표기 (Attribution): RAG 등의 환경에서 근거 문서를 정확히 참조하는가

5. 안전성 (Safety): 유해하거나 편향된 내용을 포함하고 있지 않은가 (또는 사용자 의도 이해)


2. LLM-as-a-Judge의 장점과 주의할 한계(편향)를 각각 설명하고, 편향을 완화하는 방법을 하나 제안해 보세요.
- 장점: 인간 평가자보다 10~100배 빠르고 비용이 저렴하면서도, 인간의 평가 결과와 높은 상관관계(0.7~0.9)를 가집니다.

- 한계(편향): 평가를 수행하는 LLM 자체의 편향이 개입될 수 있습니다. 가장 대표적인 것이 내용의 질과 무관하게 긴 답변에 더 높은 점수를 주는 '길이 편향(Length Bias)'입니다.

- 완화 방법: 평가 프롬프트를 작성할 때 "길이에 관계없이 핵심 내용만 평가하라"는 명시적인 지시(Instruction)를 포함하여 편향을 통제합니다.


3. 입력 드리프트, 출력 드리프트, 성능 드리프트의 차이를 각각 한 문장으로 설명하고, 자신의 프로젝트에서 가장 가능성 높은 드리프트 유형은 무엇인지 분석해 보세요.
- 입력 드리프트 (Input/Feature Drift): 모델에 들어오는 입력 데이터의 통계적 분포(예: 사용자 연령대 변화, 계절 변화) 자체가 학습 시점과 달라지는 현상입니다.

- 출력 드리프트 (Prediction Drift): 모델의 예측 결과(출력) 확률 분포가 변하는 현상입니다 (예: 갑자기 특정 클래스만 90% 비율로 예측).

- 성능 드리프트 (Performance/Concept Drift): 실제 정답(Ground Truth)과 비교했을 때 시간에 따라 실제 모델의 성능 메트릭이 직접적으로 저하되는 현상입니다.

- 내 프로젝트 분석 (예시): 텍스트 기반 챗봇이나 분류기 프로젝트라면, 시간이 지남에 따라 사용자들의 관심사, 유행어, 질문 패턴이 변화하므로 데이터 분포 자체가 달라지는 입력 드리프트가 발생할 가능성이 가장 높습니다.

4. "모델은 시간이 지나면 썩는다"는 말의 의미를 코로나19 같은 구체적 사례로 설명할 수 있으신가요? 이를 방지하기 위해 어떤 시스템이 필요한가요?
- 의미 및 사례: 소프트웨어 코드는 한 줄도 바뀌지 않았음에도, 외부 세계의 환경과 트렌드가 변하면서 모델의 성능이 저하되는 현상을 뜻합니다. 코로나19 팬데믹 당시 사람들의 행동 및 소비 패턴이 급격히 변하면서, 팬데믹 이전 데이터로 학습된 이커머스 추천 시스템이나 항공 수요 예측 모델이 하루아침에 무용지물이 된 것이 대표적인 사례입니다.

- 필요한 시스템: 모니터링 대시보드를 수동으로 보는 것을 넘어, 분포 변화가 임계값을 초과하면 즉각적으로 이메일이나 슬랙으로 경고를 보내는 실시간 자동 알림 모니터링 시스템이 필요합니다. 또한 드리프트가 확인되었을 때 최신 운영 데이터로 모델을 업데이트하는 재학습 파이프라인이 갖춰져야 합니다.





✅ Day 3 통합 체크포인트 — 3일간의 여정을 하나로 꿰기

1. 워크시트 완성: Chapter 16.3의 "나만의 Full Stack ML 프로젝트 설계 워크시트" Part A~D를 모두 채워보세요. 빈칸을 채울 수 없는 항목이 있다면, 그것이 여러분이 추가로 조사해야 할 부분입니다.

- 기획 (Part A): 한국어 뉴스 텍스트를 입력받아 7개 카테고리(정치, 경제, IT 등)로 자동 분류하는 시스템. 규칙 기반(Rule-based)으로는 신조어나 복잡한 문맥 파악에 한계가 있으므로, 사전 학습된 언어 모델(Transformers, BERT 등)을 Fine-tuning하여 도입합니다.

- 데이터 (Part B): AI Hub 및 웹 크롤링 데이터 10만 건 확보 (학습 8만, 검증 1만, 테스트 1만).

- 인프라 (Part C): PyTorch Lightning과 Hugging Face 생태계를 활용하여 학습 코드를 모듈화하고, GPU 환경(Local 또는 Colab)에서 학습을 진행합니다.

- 배포 (Part D): 학습된 모델 파라미터를 저장한 뒤, FastAPI를 이용해 실시간 텍스트 분류를 수행하는 REST API 형태로 배포합니다.


2. 테스트 전략 설계: 워크시트 Part C에서 설계한 테스트들을 구체적인 pytest 코드로 작성해 보세요. 데이터 기댓값 테스트 3개, 암기 테스트 1개, 행동 테스트 2개가 최소 목표입니다.

- 데이터 기댓값 테스트 (3개):

'''
Python
# 1. 결측치 테스트 (스모크 테스트)
assert df['text'].isnull().sum() == 0, "텍스트 컬럼에 결측치가 있습니다."

# 2. 레이블 유효성 테스트 (느슨한 경계)
assert df['label'].isin([0, 1, 2, 3, 4, 5, 6]).all(), "정의되지 않은 카테고리 레이블이 존재합니다."

# 3. 최소 데이터 길이 테스트
assert df['text'].str.len().min() >= 10, "10자 미만의 너무 짧은 노이즈 기사가 포함되어 있습니다."
'''

- 암기 테스트 (1개):

'''
Python
# 1개 배치에 대한 오버피팅 가능성 검증 (모델 파이프라인 단절 확인)
trainer = pl.Trainer(overfit_batches=1, max_epochs=50)
trainer.fit(model, train_loader)
# 훈련 종료 후 Loss가 0에 가깝게 수렴하는지 assert로 확인
'''

- 행동 테스트 (2개):

'''
Python
# 1. 불변성 테스트 (어미 변경에 대한 강건성)
score_a = model.predict("이 기술은 향후 IT 산업을 주도할 것입니다.")
score_b = model.predict("이 기술은 향후 IT 산업을 주도할 것이다.")
assert score_a == score_b, "어미가 변경되었다고 카테고리 예측이 달라집니다."

# 2. 방향성/강건성 테스트 (무관한 텍스트 추가)
base_score = model.predict_proba("금리 인상으로 인한 증시 하락세")
noisy_score = model.predict_proba("금리 인상으로 인한 증시 하락세 [광고]구독부탁")
assert abs(base_score - noisy_score) < 0.1, "노이즈 삽입 시 예측 확률이 너무 크게
'''


3. 병목 예측: 프로파일링 전에, 자신의 프로젝트에서 가장 큰 병목이 무엇일지 가설을 세워 보세요. 그리고 그 가설을 어떻게 검증할 수 있는지 구체적으로 계획하세요.

- 가설 설정: NLP 텍스트 분류 프로젝트의 특성상, Hugging Face Tokenizer를 거치는 전처리 로직이 CPU 자원을 많이 소모하여 GPU가 대기하는 '데이터 굶주림(Data Starvation)' 현상이 가장 큰 병목일 것으로 예상합니다.

- 검증 및 해결 계획: pl.Trainer(profiler="simple")을 설정하여 프로파일링을 실행한 뒤, get_train_batch (데이터 로드 및 토큰화) 소요 시간과 training_step (GPU 연산) 시간을 비교합니다. 데이터 로드 비중이 높다면 DataLoader의 num_workers를 조정하고, 그래도 부족하다면 텍스트 토큰화를 실시간으로 하지 않고 사전에 처리하여(.pt 또는 .arrow로 저장) 디스크에서 바로 읽어오도록 파이프라인을 수정합니다.

4. 1페이지 요약: 완성된 워크시트를 1페이지로 요약해 보세요. 이것을 팀원이나 멘토에게 보여주고 피드백을 받을 수 있을 정도로 명확해야 합니다. 이것이 여러분의 Full Stack ML 프로젝트의 출발점이 됩니다.
- 프로젝트 한 줄 요약: "사전 학습된 언어 모델을 Fine-tuning하여 뉴스 기사를 정확하게 분류하며, 기댓값/행동 테스트로 신뢰성을 확보하고 토큰화 병목을 최적화해 안정적으로 서비스할 수 있는 분류 API"

- 코드 뼈대 (구현 시작점):

data.py: LightningDataModule 상속. setup()에서 Tokenizer 적용, train_dataloader() 등에서 num_workers 및 pin_memory=True 설정.

model.py: LightningModule 상속. AutoModelForSequenceClassification 로드 및 training_step, 옵티마이저 설정.

train.py: Trainer 설정 (혼합 정밀도 precision="16-mixed" 적용) 및 학습 루프 실행.

tests/: 위에서 설계한 pytest 기반의 검증 스크립트 작성.


5. 코드 예시 참고: 별도 제공되는 "뉴스 분류 프로젝트 코드 예시"를 참고하여, 워크시트에서 설계한 프로젝트의 코드 구조를 구상해 보세요. LightningModule, DataModule, Trainer, test_*.py의 뼈대를 잡는 것부터 시작하면 됩니다.

1. DataModule (data.py)
데이터 로딩 병목 현상을 방지하기 위해 전처리와 병렬 로딩(num_workers, pin_memory)을 담당하는 모듈입니다.

Python
import pytorch_lightning as pl
from torch.utils.data import DataLoader
from transformers import AutoTokenizer
from datasets import load_dataset

class NewsDataModule(pl.LightningDataModule):
    def __init__(self, model_name="klue/bert-base", batch_size=32):
        super().__init__()
        self.model_name = model_name
        self.batch_size = batch_size
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def setup(self, stage=None):
        # 데이터 로드 및 토큰화 진행
        dataset = load_dataset("ynat")  # 한국어 주제 분류 뉴스 데이터셋 예시
        
        def tokenize_func(examples):
            return self.tokenizer(examples["title"], padding="max_length", truncation=True)
            
        tokenized_datasets = dataset.map(tokenize_func, batched=True)
        tokenized_datasets.set_format("torch")
        
        self.train_dataset = tokenized_datasets["train"]
        self.val_dataset = tokenized_datasets["validation"]

    def train_dataloader(self):
        # 병목 예측 가설에 따라 CPU 데이터 로딩 최적화 적용
        return DataLoader(
            self.train_dataset, 
            batch_size=self.batch_size, 
            num_workers=4,          # CPU 코어에 맞게 조절
            pin_memory=True,        # 비동기 전송
            persistent_workers=True # 워커 초기화 오버헤드 방지
        )
2. LightningModule (model.py)
순전파(Forward)와 손실 함수(Loss), 옵티마이저 등 모델의 핵심 학습 로직을 정의합니다.

Python
import pytorch_lightning as pl
import torch
from transformers import AutoModelForSequenceClassification

class NewsClassifier(pl.LightningModule):
    def __init__(self, model_name="klue/bert-base", num_labels=7, lr=2e-5):
        super().__init__()
        self.lr = lr
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name, num_labels=num_labels
        )

    def forward(self, input_ids, attention_mask):
        return self.model(input_ids=input_ids, attention_mask=attention_mask).logits

    def training_step(self, batch, batch_idx):
        logits = self(batch["input_ids"], batch["attention_mask"])
        loss = torch.nn.functional.cross_entropy(logits, batch["label"])
        self.log("train_loss", loss, on_step=True, on_epoch=True)
        return loss

    def configure_optimizers(self):
        # OOM 및 성능 최적화를 고려한 AdamW 적용
        return torch.optim.AdamW(self.parameters(), lr=self.lr)
3. Trainer 및 실행부 (train.py)
작성한 모듈들을 조립하고, OOM 방지 및 빠른 실험을 위한 설정을 주입하여 학습을 실행합니다.

Python
import pytorch_lightning as pl
from model import NewsClassifier
from data import NewsDataModule

def main():
    data_module = NewsDataModule(batch_size=32)
    model = NewsClassifier()

    trainer = pl.Trainer(
        max_epochs=5,
        accelerator="auto",
        precision="16-mixed",         # OOM 방지 및 연산 속도 최적화 (Make it Fast)
        profiler="simple",            # 병목 지점(get_train_batch vs training_step) 확인
        gradient_clip_val=1.0         # NaN/Inf 폭주 방지
    )
    
    trainer.fit(model, datamodule=data_module)

if __name__ == "__main__":
    main()
4. 테스트 코드 (tests/test_model.py)
모델이 훈련 환경에 올라가기 전에 기초 배관이 연결되었는지 확인하는 단위 테스트입니다.

Python
import pytest
import torch
from model import NewsClassifier

@pytest.fixture
def sample_batch():
    """테스트용 가짜 배치 데이터 (Batch Size: 8)"""
    input_ids = torch.randint(0, 1000, (8, 128))
    attention_mask = torch.ones(8, 128)
    labels = torch.randint(0, 7, (8,))
    return {"input_ids": input_ids, "attention_mask": attention_mask, "label": labels}

def test_model_output_shape(sample_batch):
    """레이어 연결 및 브로드캐스팅 오류 검증 (Shape 테스트)"""
    model = NewsClassifier(num_labels=7)
    logits = model(sample_batch["input_ids"], sample_batch["attention_mask"])
    
    assert logits.shape == (8, 7), f"Expected (8, 7), but got {logits.shape}"

def test_model_no_nan_output(sample_batch):
    """수치적 불안정성으로 인한 NaN 발생 여부 검증"""
    model = NewsClassifier(num_labels=7)
    logits = model(sample_batch["input_ids"], sample_batch["attention_mask"])
    
    assert torch.isfinite(logits).all(), "NaN or Inf detected in model output"
위 뼈대 코드를 기반으로 프로젝트의 실제 모델명(Hugging Face 경로)과 커스텀 데이터셋을 교체하면, 설계하신 워크시트 내용대로 즉시 실험(Make it Run)을 시작할 수 있습니다.
