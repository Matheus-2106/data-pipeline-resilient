from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import router as api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="API para recepção e orquestração de pipelines de dados em larga escala de forma assíncrona."
)

# Inclui as rotas com prefixo /api/v1
app.include_router(api_router, prefix=settings.API_V1_STR, tags=["Data Pipeline"])


@app.get("/healthcheck", tags=["Health"])
async def health_check():
    return {"status": "ok", "version": settings.PROJECT_VERSION}