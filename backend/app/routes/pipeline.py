from fastapi import APIRouter
from app.services.pipeline_service import run_pipeline

router = APIRouter()

@router.get("/run-pipeline")
def execute_pipeline():
    return run_pipeline()