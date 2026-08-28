from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import joblib
import numpy as np

app = FastAPI()
model = joblib.load('model.joblib')

class PredictRequest(BaseModel):
    data: List[float]

@app.post("/predict")
def predict(request: PredictRequest):
    # 입력 데이터는 request.data에 담겨 옵니다.
    prediction = model.predict([request.data])
    return {"class_index": int(prediction[0])}