from contextlib import asynccontextmanager
from fastapi import FastAPI
from utils.decorators import repeatEvery



# task to be repeated every x seconds
@repeatEvery(seconds=5)
async def fetchYoutubeData():
    print('Running fetchYoutubeData\n')



@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialization
    await fetchYoutubeData()
    yield
    # cleanup