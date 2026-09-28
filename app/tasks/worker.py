import random
import time
from typing import Any, Dict
from celery.utils.log import get_task_logger
from app.core.celery_app import celery_app
from app.core.exceptions import InvalidDataPayloadError, TransientNetworkError

logger = get_task_logger(__name__)


@celery_app.task(
    bind=True,
    name="process_data_chunk",
    max_retries=3,
    default_retry_delay=2,
    autoretry_for=(TransientNetworkError,),
    retry_backoff=True,        # Exponencial Backoff (2s, 4s, 8s...)
    retry_backoff_max=60,      # Limite máximo de espera
    retry_jitter=True          # Adiciona jitter aleatório às retentativas
)
def process_data_chunk(self, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processa um lote de dados de forma assíncrona e resiliente.
    Aplica mecanismo de retry automático para falhas transitórias.
    """
    source_id = payload.get("source_id")
    records_count = payload.get("records_count", 0)
    attempt = self.request.retries + 1

    logger.info(f"[Tentativa {attempt}] Iniciando processamento do lote '{source_id}' com {records_count} registros.")

    if source_id.startswith("FAIL"):
        logger.error(f"Erro fatal: Fonte de dados '{source_id}' bloqueada ou corrompida.")
        raise InvalidDataPayloadError(f"A fonte '{source_id}' contém dados irrecoveráveis.")

    if payload.get("simulate_flaky_network") and random.random() < 0.30:
        logger.warning(f"[Tentativa {attempt}] Falha temporária simulada na conexão para '{source_id}'.")
        raise TransientNetworkError("Instabilidade temporária de rede detectada.")

    time.sleep(2)

    return {
        "status": "COMPLETED",
        "attempt": attempt,
        "processed_records": records_count,
        "source_id": source_id,
        "summary": f"Processados {records_count} registros com sucesso da fonte '{source_id}' na tentativa {attempt}."
    }