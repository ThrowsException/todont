from fastapi import FastAPI
from uvicorn import run

from backend.app.routers import todos

app = FastAPI(title="TODONT API")

app.include_router(todos.router)


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
