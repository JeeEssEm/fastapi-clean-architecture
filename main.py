from routers import users, news, comments, auth
from config import settings
from database import init_models

import asyncio
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette import status

app = FastAPI(
    title='Coffee  backend'
)


app.include_router(auth)
app.include_router(users)
app.include_router(news)
app.include_router(comments)


@app.get('/')
async def root():
    return 'ok'


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request, exc: ValidationError,
):
    errors = exc.errors()[0]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            'detail': f'{errors["msg"]}: {errors["loc"][-1]}'
        }
    )

if __name__ == '__main__':
    if settings.INIT_MODELS:
        asyncio.run(init_models())

    uvicorn.run('main:app',
                host=settings.HOST, port=settings.PORT, reload=True)
