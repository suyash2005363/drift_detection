from fastapi import FastAPI
from app.routes import predict, dashboard, pipeline

app = FastAPI(title="Drift Detection API")

app.include_router(predict.router)
app.include_router(dashboard.router)
app.include_router(pipeline.router)

@app.get("/")
def home():
    return {"message": "API is running 🚀"}