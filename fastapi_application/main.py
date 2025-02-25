from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends

from config import settings
from api.views import router as api_router
from db_helper import db_helper
from dependencies import validate_api_key


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan, dependencies=[Depends(validate_api_key)])
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        host=settings.run.host,
        port=settings.run.port,
    )
