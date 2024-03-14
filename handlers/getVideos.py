from db import sessionManager
from models import Video
from utils.asyncUtils import asyncWrapper
import asyncio


def getVideosSync(page: int, limit: int):
    with sessionManager() as session:
        res = session.query(Video).order_by(Video.published_at.desc()).limit(limit).offset((page-1)*limit)
        return res


async def getVideos(page: int, limit: int):
    # running it in the event_loop's theadpool executor to not block the currently running event loop
    res = await asyncWrapper(getVideosSync, page=page, limit=limit)
    videos = [r.getMapping() for r in res]
    return {
        'page': page,
        'limit': limit,
        'numVideos': len(videos),
        'videos': videos
    }




if __name__=='__main__':
    data = asyncio.run(getVideos(page=1, limit=50))
    print(data)