from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import tensorflow as tf

app = FastAPI()

# 1. Load artifacts on startup

model = tf.keras.models.load_model('/app/artifacts/stroke_nn_model.keras')
scaler = joblib.load('/app/artifacts/scaler.joblib')

# 2. Define input schema
class StrokeFeatures(BaseModel):
    gender: int
    age: float
    hypertension: int
    heart_disease: int
    ever_married: int
    work_type: int
    Residence_type: int
    avg_glucose_level: float
    bmi: float
    smoking_status: int

# 3. Create endpoint
@app.post("/predict")
def predict_stroke_endpoint(features: StrokeFeatures):
    # Convert Pydantic model to list/array
    raw_features = [
        features.gender, features.age, features.hypertension, 
        features.heart_disease, features.ever_married, features.work_type,
        features.Residence_type, features.avg_glucose_level, features.bmi, 
        features.smoking_status
    ]
    
    features_array = np.array(raw_features).reshape(1, -1)
    scaled_features = scaler.transform(features_array)
    
    probability = model.predict(scaled_features, verbose=0)[0][0]
    classification = 1 if probability >= 0.5 else 0
    
    return {"probability": float(probability), "stroke_prediction": classification}