from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Query, HTTPException
import traceback
from lifespan import lifespan
from handlers import getVideos as getVideosHandler, searchQuery as searchQueryHandler


app = FastAPI(lifespan=lifespan)


@app.get('/health_check')
async def root():
    return {'message': 'Hello world'}




@app.get('/videos')
async def getVideos(page: int  = Query(1), limit: int = Query(50)):
    try:
        data = await getVideosHandler(page=page, limit=limit)
        return data
    except Exception as e:
        print(traceback.format_exc())
        errorMsg = f'Error: {e}'
        raise HTTPException(status_code=500, detail=errorMsg)





@app.get('/search')
async def searchQuery(q: str = Query(''), limit: int = Query(50)):
    try:
        data = await searchQueryHandler(q=q, lim=limit)
        return data
    except Exception as e:
        print(traceback.format_exc())
        errorMsg = f'Error: {e}'
        raise HTTPException(status_code=500, detail=errorMsg)

    