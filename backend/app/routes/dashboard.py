from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
def dashboard():
    return {
        "drift": False,
        "confidence": 0.85,
        "alerts": [],
        "status": "All systems normal"
    }