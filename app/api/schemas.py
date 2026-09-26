from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class DataPayload(BaseModel):
    source_id: str = Field(..., description="Identificador da fonte dos dados")
    records_count: int = Field(..., gt=0, description="Quantidade de registros a processar")
    payload_data: Dict[str, Any] = Field(..., description="Conteúdo dos dados em formato JSON")

    model_config = {
        "json_schema_extra": {
            "example": {
                "source_id": "SRC-9876",
                "records_count": 1500,
                "payload_data": {"category": "financial_report", "period": "2026-Q3"}
            }
        }
    }


class JobResponse(BaseModel):
    task_id: str
    status: TaskStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)
    message: str


class JobStatusResponse(BaseModel):
    task_id: str
    status: TaskStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None