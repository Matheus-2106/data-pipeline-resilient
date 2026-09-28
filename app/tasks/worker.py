import time
from typing import Any, Dict
from app.core.celery_app import celery_app


@celery_app.task(bind=True, name="process_data_chunk")
def process_data_chunk(self, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simula uma tarefa pesada de processamento de dados (ex: ETL, cálculo, consulta a banco).
    """
    source_id = payload.get("source_id")
    records_count = payload.get("records_count", 0)

    # Simula processamento demorado
    processing_time = max(2, records_count // 500)
    time.sleep(processing_time)

    # Resultado do processamento
    return {
        "status": "COMPLETED",
        "processed_records": records_count,
        "source_id": source_id,
        "summary": f"Processados {records_count} registros com sucesso da fonte '{source_id}'."
    }