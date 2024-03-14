from db import engine
from utils.asyncUtils import asyncWrapper
from sqlalchemy import text
import asyncio


def searchQuerySync(q: str, lim: int):
    query = f"SELECT * from videos WHERE MATCH(title, description) AGAINST('{q}') LIMIT {lim}"
    with engine.connect() as conn:
        res = conn.execute(text(query))
        return res


async def searchQuery(q: str, lim: int):
    # running it in the event_loop's theadpool executor to not block the currently running event loop
    res = await asyncWrapper(searchQuerySync, q=q, lim=lim)
    videos = []
    for r in res:
        videos.append({
            'video_id': r[0],
            'title': r[1],
            'description': r[2],
            'published_at': r[3],
            'thumbnail_url': r[4]
        })
    return {
        'numVideos': len(videos),
        'videos': videos
    }


if __name__=='__main__':
    res = asyncio.run(searchQuery(q='ronaldo', lim=10))
    print(res)