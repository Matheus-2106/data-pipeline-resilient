import uuid
from fastapi import APIRouter, HTTPException, status
from app.api.schemas import DataPayload, JobResponse, JobStatusResponse, TaskStatus

router = APIRouter()

# Banco em memória simulado apenas para testes preliminares do Commit 2
# No próximo commit, conectaremos isto ao Celery e Redis
DUMMY_JOBS_DB = {}


@router.post("/process-data", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED)
async def submit_data_processing(payload: DataPayload):
    """
    Recebe uma carga de dados pesada para processamento assíncrono.
    Retorna 202 Accepted imediatamente com o ID da tarefa.
    """
    task_id = str(uuid.uuid4())

    # Armazena status inicial simulado
    DUMMY_JOBS_DB[task_id] = {
        "status": TaskStatus.PENDING,
        "payload": payload.model_dump()
    }

    return JobResponse(
        task_id=task_id,
        status=TaskStatus.PENDING,
        message="Tarefa enviada para a fila de processamento assíncrono com sucesso."
    )


@router.get("/process-data/{task_id}", response_model=JobStatusResponse)
async def get_processing_status(task_id: str):
    """
    Consulta o status de execução de uma tarefa enviada previamente.
    """
    job = DUMMY_JOBS_DB.get(task_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID '{task_id}' não encontrada."
        )

    return JobStatusResponse(
        task_id=task_id,
        status=job["status"],
        result=job.get("result"),
        error=job.get("error")
    )