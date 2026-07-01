from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Any
import sys
sys.path.append('/app')
from common.queue import JobQueue

router = APIRouter()

class JobSubmit(BaseModel):
    number: int

@router.post("/submit")
async def submit_job(job: JobSubmit):
    queue = JobQueue()
    job_id = queue.submit_job({"number": job.number})
    return {"job_id": job_id, "status": "queued"}

@router.get("/status/{job_id}")
async def get_job_status(job_id: str):
    queue = JobQueue()
    status = queue.get_job_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return status

@router.get("/queue-length")
async def get_queue_length():
    queue = JobQueue()
    return {"queue_length": queue.get_queue_length()}
