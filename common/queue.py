import redis
import json
import uuid
import os
from typing import Optional, Dict, Any

class JobQueue:
    def __init__(self, redis_host: str = None, redis_port: int = 6379):
        if redis_host is None:
            redis_host = os.getenv('REDIS_HOST', 'redis')
        self.redis = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.queue_key = 'job_queue'
        self.status_key_prefix = 'job_status:'

    def submit_job(self, job_data: Dict[str, Any]) -> str:
        job_id = str(uuid.uuid4())
        job = {
            'id': job_id,
            'status': 'queued',
            'data': job_data,
            'result': None,
            'error': None
        }
        self.redis.lpush(self.queue_key, json.dumps(job))
        self._update_status(job_id, job)
        return job_id

    def pop_job(self) -> Optional[Dict[str, Any]]:
        job_json = self.redis.brpop(self.queue_key, timeout=1)
        if job_json:
            job = json.loads(job_json[1])
            job['status'] = 'running'
            self._update_status(job['id'], job)
            return job
        return None

    def complete_job(self, job_id: str, result: Any = None, error: str = None):
        job = self.get_job_status(job_id) or {}
        status = 'completed' if error is None else 'failed'
        job['status'] = status
        job['result'] = result
        job['error'] = error
        self._update_status(job_id, job)

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        status_json = self.redis.get(f"{self.status_key_prefix}{job_id}")
        if status_json:
            return json.loads(status_json)
        return None

    def get_queue_length(self):
        return self.redis.llen(self.queue_key)

    def _update_status(self, job_id: str, job_data: Dict[str, Any]):
        self.redis.set(f"{self.status_key_prefix}{job_id}", json.dumps(job_data))
