import uvicorn
from fastapi import FastAPI

from hotels import router as router_hotels

app = FastAPI()
app.include_router(router_hotels)


if __name__ == "__main__":
    uvicorn.run(
        app     = "main:app",
        host    = "0.0.0.0",
        port    = 8000,
        reload  = True
    )