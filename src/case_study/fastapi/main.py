from fastapi import FastAPI
from .routers import portfolios
import uvicorn

app = FastAPI(title="FintelaAI Portfolio API")

app.include_router(portfolios.router)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("src.case_study.fastapi.main:app", host="0.0.0.0", port=8000, reload=True)
