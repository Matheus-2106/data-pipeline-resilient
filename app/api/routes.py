from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, status
from app.api.schemas import DataPayload, JobResponse, JobStatusResponse, TaskStatus
from app.core.celery_app import celery_app
from app.tasks.worker import process_data_chunk

router = APIRouter()


@router.post("/process-data", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED)
async def submit_data_processing(payload: DataPayload):
    """
    Envia uma carga de dados para a fila do Redis para processamento assíncrono via Celery.
    """
    # Envia a tarefa para a fila do Celery (.delay)
    task = process_data_chunk.delay(payload.model_dump())

    return JobResponse(
        task_id=task.id,
        status=TaskStatus.PENDING,
        message="Tarefa enviada para a fila de processamento assíncrono com sucesso."
    )


@router.get("/process-data/{task_id}", response_model=JobStatusResponse)
async def get_processing_status(task_id: str):
    """
    Consulta o estado de execução no Redis a partir do task_id.
    """
    task_result = AsyncResult(task_id, app=celery_app)

    # Mapeamento do status nativo do Celery para o nosso Enum do Pydantic
    celery_state = task_result.state
    if celery_state == "PENDING":
        job_status = TaskStatus.PENDING
    elif celery_state in ["STARTED", "RETRY"]:
        job_status = TaskStatus.PROCESSING
    elif celery_state == "SUCCESS":
        job_status = TaskStatus.SUCCESS
    else:
        job_status = TaskStatus.FAILED

    response = JobStatusResponse(
        task_id=task_id,
        status=job_status
    )

    if task_result.ready():
        if task_result.successful():
            response.result = task_result.result
        else:
            response.error = str(task_result.result)

    return response