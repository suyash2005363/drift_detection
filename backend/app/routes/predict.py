from fastapi import APIRouter
from app.services.model_service import predict_output

router = APIRouter()   # ✅ THIS LINE IS IMPORTANT

@router.post("/predict")
def predict(data: dict):
    return predict_output(data)