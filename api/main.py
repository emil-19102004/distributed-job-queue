from fastapi import FastAPI
import sys
sys.path.append('/app')
from api.routes import router

app = FastAPI(title="Distributed Job Queue")

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Job Queue API is running"}
