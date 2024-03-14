from contextlib import asynccontextmanager
from fastapi import FastAPI
from handlers.fetchAndUpdateYoutubeData import fetchAndUpdateYoutubeData





@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialization
    await fetchAndUpdateYoutubeData()
    print('Initialization of fastapi server done')
    yield
    # cleanup