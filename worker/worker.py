import time
import sys
sys.path.append('/app')
from common.queue import JobQueue

def is_prime(n: int) -> bool:
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def count_primes(n: int) -> int:
    return sum(1 for i in range(2, n + 1) if is_prime(i))

def process_job(job: dict):
    try:
        data = job.get('data', {})
        number = data.get('number', 10000)
        job_id = job['id']
        print(f"[WORKER] STARTED job {job_id} with n={number}")
        start = time.time()
        result = count_primes(number)
        duration = time.time() - start
        print(f"[WORKER] COMPLETED job {job_id} in {duration:.2f}s | Primes: {result}")
        return result
    except Exception as e:
        print(f"[WORKER] ERROR in job {job.get('id')}: {e}")
        raise

if __name__ == "__main__":
    queue = JobQueue()
    print("🚀 Worker started and waiting for jobs...")
    while True:
        job = queue.pop_job()
        if job:
            try:
                result = process_job(job)
                queue.complete_job(job['id'], result=result)
                print(f"[WORKER] Job {job['id']} marked as completed")
            except Exception as e:
                queue.complete_job(job['id'], error=str(e))
                print(f"[WORKER] Job {job.get('id')} marked as failed")
