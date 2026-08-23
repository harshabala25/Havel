from fastapi import FastAPI
import joblib
import pandas as pd
import json
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

model = joblib.load('rent_model.pkl')

with open('model_columns.json', 'r') as f:
    model_columns = json.load(f)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://havel.vercel.app",  # replace with your actual frontend URL once deployed
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RentRequest(BaseModel):
    zip_code: str
    bedrooms: int

@app.get("/")
def home():
    return {"message": "Rent predictor API is running"}

@app.post("/predict")
def predict_rent(request: RentRequest):
    input_data = pd.DataFrame(columns=model_columns)
    input_data.loc[0] = 0

    input_data['bedrooms'] = request.bedrooms
    zip_column = f"zip_code_{request.zip_code}"

    if zip_column in model_columns:
        input_data[zip_column] = 1

    prediction = model.predict(input_data)
    
    return {"predicted_rent": float(prediction[0])}