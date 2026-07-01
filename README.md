# Distributed Job Queue

A scalable, distributed background job processing system built with **FastAPI**, **Redis**, **Docker**, and **Kubernetes**.

## Features

- REST API for job submission and status tracking
- Redis-based message queue with LPUSH/BRPOP
- Multiple concurrent worker processes
- Containerized with Docker
- Horizontal scaling with Kubernetes
- Fault-tolerant job processing
- Real-time job status updates

## Tech Stack

- **Backend**: FastAPI + Python
- **Queue**: Redis
- **Task**: Prime number counting (CPU intensive)
- **Container**: Docker
- **Orchestration**: Kubernetes

## Project Structure
job-queue/
├── api/                    # FastAPI application
│   ├── main.py
│   └── routes.py
├── worker/                 # Worker processes
│   └── worker.py
├── common/                 # Shared queue logic
│   └── queue.py
├── k8s/                    # Kubernetes manifests
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
text
