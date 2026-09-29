# Resilient Data Pipeline API

Um pipeline de processamento de dados assíncrono, distribuído e resiliente construído com **FastAPI**, **Celery** e **Redis**, totalmente containerizado com **Docker Compose**.

O projeto simula a recepção de grandes volumes ou cargas de dados via API e delega o processamento pesado para workers em segundo plano, aplicando padrões de **Exponential Backoff com Jitter** para garantir alta tolerância a falhas temporárias de rede ou infraestrutura.

---

## Tecnologias Utilizadas

* **Linguagem:** Python 3.11
* **API Framework:** FastAPI & Pydantic v2
* **Asynchronous Task Queue:** Celery 5.x
* **Message Broker & Result Backend:** Redis (Alpine)
* **Containerização & Orquestração:** Docker & Docker Compose
* **Servidor ASGI:** Uvicorn

---

## Recursos de Resiliência & Padrões Arquiteturais

1. **Processamento Assíncrono:** Desacoplamento total entre a camada HTTP e o processamento pesado de dados.
2. **Exponential Backoff:** Retentativas automáticas em intervalos crescentes (2s, 4s, 8s...) em caso de erros temporários (`TransientNetworkError`).
3. **Retry Jitter:** Adição de variações aleatórias aos tempos de retentativa para evitar acoplamento temporal das conexões (*Thundering Herd Problem*).
4. **Isolamento de Exceções:** Diferenciação clara entre erros transitórios (recuperáveis via retry) e falhas fatais de dados (`InvalidDataPayloadError`).
5. **Ambiente Reprodutível:** Orquestração completa de multi-containers com verificação de *healthcheck* do Redis antes de subir a API e o Worker.

---

## Como Executar o Projeto

### Pré-requisitos
* **Docker** e **Docker Compose** instalados.

### Passos
1. Clone este repositório:
   ```bash
   git clone https://github.com/matheus-2106/data-pipeline-resilient.git
   cd data-pipeline-resilient
   ```

2. Suba o ambiente completo com apenas um comando:
   ```bash
   docker compose up --build
   ```

3. Acesse a documentação interativa da API no navegador:
   👉 **`http://127.0.0.1:8000/docs`**

---

## Como Testar no Swagger UI

### 1. Enviar um Lote de Dados (`POST /api/v1/process-data`)
Envie a requisição de exemplo:
```json
{
  "source_id": "SRC-9876",
  "records_count": 1500,
  "payload_data": {
    "category": "financial_report",
    "period": "2026-Q3"
  },
  "simulate_flaky_network": true
}
```
* **Teste de Retry:** Ao marcar `"simulate_flaky_network": true`, a tarefa simula oscilações de rede. Acompanhe no terminal as retentativas automáticas sendo tratadas pelo Celery.
* **Teste de Erro Fatal:** Se utilizar `"source_id": "FAIL-123"`, o sistema identifica erro irrecuperável e interrompe o job imediatamente sem retentativas.

### 2. Consultar Status da Tarefa (`GET /api/v1/tasks/{task_id}`)
Utilize o `task_id` retornado no POST para acompanhar a mudança de estado de `PENDING` para `SUCCESS` ou `FAILED`.