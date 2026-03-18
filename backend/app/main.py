from fastapi import FastAPI
from uvicorn import run
from fastapi_mcp import FastApiMCP

from backend.app.routers import todos

app = FastAPI(title="TODONT API")

mcp = FastApiMCP(app)

# Mount the MCP server directly to your FastAPI app
mcp.mount_http()

app.include_router(todos.router)


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
