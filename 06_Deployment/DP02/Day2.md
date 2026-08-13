
## 섹션 1.5 수행내역 캡쳐
<img width="632" height="1311" alt="day2_FastAPI" src="https://github.com/user-attachments/assets/bdeeb37e-965f-44c5-9789-7346c21aab9a" />  



## 섹션 2, 3 셀 출력 
<img width="691" height="615" alt="day2_Section 2_body" src="https://github.com/user-attachments/assets/084c4f4e-2a4b-4354-a8d6-9bcb7106347e" />
<img width="544" height="755" alt="day2_section2_path_query" src="https://github.com/user-attachments/assets/cfe547d7-3665-4838-ba1c-e84af192f062" />
<img width="705" height="636" alt="day2_section3_openapi" src="https://github.com/user-attachments/assets/791d543b-74d5-4499-8e3b-32e80190e82f" />


## 섹션 5 수행내역 캡쳐
<img width="1148" height="1926" alt="day2_POST422" src="https://github.com/user-attachments/assets/ea3ea0fc-45b3-4516-a4ed-5a2acd29da4b" />
<img width="1145" height="1780" alt="day2_POST200" src="https://github.com/user-attachments/assets/b375c5f3-f81b-41cd-9ba5-8e3630986dd4" />
<img width="1148" height="967" alt="day2_GET200" src="https://github.com/user-attachments/assets/9687a36c-4dc3-404d-80d3-03f3a8ff4050" />






---

✅ 체크포인트
다음 질문에 답할 수 있다면, 이 섹션의 학습 목표를 달성한 것입니다:

1. FastAPI가 Flask보다 모델 배포에 적합한 이유 세 가지는 무엇입니까?  
- 모델 베포에서 자주 필요한 기능들이 기본 내장되어 있기 때문: Pydantic 자동 검증   
- 코드를 작성하면 API 문서가 자동으로 생성(swagger)  
- 비동기 기반으로 작업하므로 동시에 여러 요청을 처리할 수 있다.  

2. Uvicorn의 역할은 무엇이며, 왜 FastAPI와 함께 사용합니까?  
- HTTP 요청을 받아서 FastAPI에 전달하는 역할로 웹 서버의 '문지기'라고 생각하면 된다.  
- FastAPI 자체는 요청을 받는 기능이 없어 Uvicorn이 있어야한다.  
: FastAPI는 API를 만드는 프레임워크이고, Uvicorn은 그 API를 실제로 실행해주는 웹 서버다.  

3. @app.get("/health")에서 get과 "/health"는 각각 무엇을 의미합니까?  
- HTTP 메서드 : GET  
- URL 경로 : /health  
: 이 선언에 의해, GET/health 요청이 들어오면 health() 함수가 실행된다.  

4. FastAPI에서 dict를 반환하면 어떤 일이 자동으로 일어납니까?  
: FastAPI는 Python의 dict을 자동으로 JSON 형식의 HTTP Response로 변환. json.dumps()를 호출할 필요가 없다.


✅ 체크포인트
다음 질문에 답할 수 있다면, 이 섹션의 학습 목표를 달성한 것입니다:

1. /models/sentiment-v1에서 sentiment-v1은 어떤 종류의 파라미터입니까?  
:  Path Parameter(경로 파라미터) — URL 경로의 일부로 전달 (특정 리소스를 식별할때 사용)   

- GET /models?name=sentiment&version=1 : Query 파라미터 — URL 뒤에 ?key=value 형태로 전달  
- POST /predict : Request Body — HTTP 요청 본문에 JSON으로 전달  

2. /models?status=running&limit=5에서 status와 limit은 어떤 종류의 파라미터입니까?  
: Query Parameter(쿼리 파라미터)
- limit : int =10 기본값이 있는 파라미터 -> 선택적(생략 가능)
- status : str = None 기본값이 None인 파라미터 -> 선택적(없으면 필터링 안 함)
- status : str 기본값이 없는 파라미터 -> 필수(생략하면 422 에러)

3. 모델 추론 요청에 Request Body를 사용하는 이유는 무엇입니까?  
: HTTP요청을 본문에 JSON 데이터를 담아 보내는 방식으로 모델 추론 요청처럼 __복잡한 데이터를 전달__할때 사용  

특히 텍스트, 이미지 정보, 여러 개의 feature, 생성 옵션 등 구조화된 데이터를 전송할 때 Body가 적합.  
FastAPI에서 Request Body를 받으려면 Pydantic 모델을 사용한다.  

4. FastAPI에서 함수의 파라미터가 Path, Query, Body 중 어디서 오는지 어떻게 판별합니까?  
- Path : URL 경로 안   /   URL에 {}로 선언되어 있으면 Path Parameter  
- Query : URL ? 뒤    /   함수 파라미터인데 URL Path에 {}로 정의되어 있지 않으면 보통 Query Parameter로 판단  
- Body : HTTP 본문 (JSON)  /  BaseModel 같은 Pydantic 모델을 함수 파라미터로 사용하면 FastAPI는 이를 Request Body로 판단  
| 구분 | 판단 방법 | 예 |
| :--- | :--- | :--- |
| **Path Parameter** | URL에 {변수}가 있음 | `/models/{model_id}` |
| **Query Parameter** | 함수 파라미터지만 Path에 없음 | `/models?limit=5` |
| **Request Body** | Pydantic BaseModel 등을 사용 | `{"text": "hello"}` |


✅ 체크포인트  
다음 질문에 답할 수 있다면, 이 섹션의 학습 목표를 달성한 것입니다:  

1. FastAPI에서 Swagger UI에 접속하려면 어떤 URL로 이동합니까?  
: http://localhost:8000/docs  

2. Swagger UI가 코드와 항상 동기화될 수 있는 이유는 무엇입니까?  
: JSON Schema를 읽어서 입력 폼을 자동으로 만들고, 사람이 Pydantic 모델을 수정하면, 문서도 자동으로 업데이트 된다. (코드와 문서가 항상 동기화)  

3. Pydantic 모델의 Field(description=, examples=)는 Swagger UI의 어디에 반영됩니까?  
: __코랩 파일에 정의된 내용__ - # Field()에 description과 examples를 추가하면 Swagger UI에 반영됩니다.  

- Swagger UI에서 해당 API의 Request Body 스키마와 예시 등에 반영됩니다.  
- description은 해당 필드가 무엇을 의미하는지 설명하고, examples는 어떤 값을 넣을 수 있는지 예시를 제공합니다.  
- API를 사용하는 사람이 코드를 직접 읽지 않아도 어떤 데이터를 보내야 하는지 이해할 수 있게 해주는 것입니다.  

4. Swagger UI와 ReDoc의 핵심 차이는 무엇입니까?  
: 가장 큰 차이는 목적과 UI  
Swagger UI = API를 직접 테스트하기 좋고 개발자가 사용  
ReDoc = API 문서를 읽기 좋고 클라이언트(외부)에서 사용  

둘 다 FastAPI가 생성한 OpenAPI 명세를 보여주는 도구  
| 기능 및 특징 | Swagger UI | ReDoc |  
| :--- | :--- | :--- |  
| **기본 URL** | `/docs` | `/redoc` |  
| **주요 용도** | API 테스트에 편리 | 문서 읽기에 편리 |  
| **상호작용** | 직접 요청을 보내볼 수 있음 | API 구조 파악에 적합 |  
| **활용 분야** | 개발·테스트에 많이 사용 | 문서 제공에 유리 |  




✅ 체크포인트  
다음 질문에 답할 수 있다면, 이 섹션의 학습 목표를 달성한 것입니다:  

1. text: str과 text: str = "기본값"의 차이는 무엇입니까?  
- text: str [타입만 선언: 필수 입력 필드]  
- text: str = "기본값" [기본값 지정: 선택적(Optional) 입력 필드]  

:  text: str은 클라이언트가 str값을 전달하지 않으면 검증 에러(422)발생,  
 text: str = "기본값"은 에러 발생하지 않고 "기본값"이 자동으로 채워져 사용  

2. Field(..., min_length=1, max_length=5000)에서 ...은 무엇을 의미합니까?  
:... 은 "필수"를 의미

3. 422 에러 응답에서 loc 필드는 어떤 정보를 담고 있습니까?  
: 에러 발생 위치 (["body", "text"] → 요청 본문의 text 필드)

4. response_model을 지정하면 어떤 이점이 있습니까?  
- Swagger UI에 응답 형식이 자동 문서화된다. 
- 내부 데이터나 민감한 정보가 클라이언트에게 실수로 노출되는 것을 방지 (지정한 Pydantic 스키마에 정의되지 않은 데이터는 실제 응답을 보낼 때 자동으로 제거)  



✅ 체크포인트  
다음 질문에 답할 수 있다면, Day 2의 학습 목표를 달성한 것입니다:  

1. 모델을 서버 시작 시 한 번만 로드해야 하는 이유는 무엇입니까?  
: 모델을 메모리에 올리는 과정은 파일 I/O가 포함된 무거운 작업입니다. 클라이언트의 요청이 들어올 때마다 매번 모델을 로드하면 응답 시간이 수 초 이상으로 크게 늘어나 정상적인 서비스가 불가능해지기 때문입니다.  

2. pixel_values가 784개가 아닌 요청이 들어오면 어떤 일이 발생합니까? 이를 처리하는 코드를 직접 작성했습니까?  
- FastAPI가 자동으로 요청을 차단하고 422 에러(Validation Error)와 함께 상세한 에러 메시지를 반환합니다.  

- 직접 if len(pixel_values) != 784:와 같은 검증 로직을 작성하지 않았습니다. Pydantic 스키마 정의 시 Field(min_length=784, max_length=784)로 규칙을 선언하기만 하면 프레임워크가 이를 대신 처리해 줍니다.  

3. HTTPException(status_code=503)은 어떤 상황에서 사용했습니까? 왜 500이 아니라 503입니까?  
- 서버 시작 시 모델 로드에 실패하여(model_loaded == False) 추론 서비스를 제공할 수 없는 상황에서 사용했습니다.  

- 500(Internal Server Error)은 로직 실행 중 발생하는 예기치 못한 내부 오류를 의미하지만, 503(Service Unavailable)은 '현재 서버가 정상적으로 요청을 처리할 준비가 되지 않았다'는 상태를 클라이언트에게 더 명확하게 전달하는 목적에 부합하기 때문입니다.  

4. Swagger UI에서 PredictRequest의 description과 examples가 어디에 표시됩니까  
-Swagger UI에서 POST /predict 항목을 열었을 때 나타나는 Request body 영역에 표시됩니다. examples는 미리 채워진 JSON 입력 폼 형태로 나타나며, description은 Schema 탭을 눌렀을 때 각 데이터 필드의 설명란에 나타납니다.
