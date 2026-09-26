import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Resilient Data Pipeline"
    PROJECT_VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Redes e Filas
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")


settings = Settings()