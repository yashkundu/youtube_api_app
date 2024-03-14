from config import config
from utils.decorators import repeatEvery
import httpx
import os
import datetime
from utils.general import recDictKeyFetcher
import asyncio
from models import Video
from db import sessionManager
import traceback



youtubeSearchUrl = 'https://www.googleapis.com/youtube/v3/search'


# TODO check response status, and also if out quota is exhausted
async def fetchYoutubeVideos(lim: int, params: dict) -> list[dict]:
    nextPageToken = None
    data = []
    firstIter = True
    # the api is returning some duplicate videos, to deal with it store the videoids in set, and only consider those videos whose video ids have not been already present in the set
    videoIdsSet = set()
    while firstIter or (len(data)<lim and nextPageToken):
        firstIter = False
        async with httpx.AsyncClient() as client:
            newParams = {**params}
            if nextPageToken:
                newParams['pageToken'] = nextPageToken
            r = await client.get(youtubeSearchUrl, params=newParams)
            d = r.json()
            nextPageToken = d.get('nextPageToken', None)
            videos = list(map(lambda x: {
                'video_id': recDictKeyFetcher(x, 'id', 'videoId'),
                'published_at': datetime.datetime.fromisoformat(recDictKeyFetcher(x, 'snippet', 'publishedAt')),
                'title': recDictKeyFetcher(x, 'snippet', 'title'),
                'description': recDictKeyFetcher(x, 'snippet', 'description'),
                'thumbnail_url': recDictKeyFetcher(x, 'snippet', 'thumbnails', 'default', 'url')
            }, d.get('items', [])))
            videos = list(filter(lambda x: x['video_id'] not in videoIdsSet, videos))
            videoIdsSet.update([video['video_id'] for video in videos])
            data.extend(videos)
    return data



# This field is used to identify if the scheduled job is invoked first time or not
x = True
isFirstInvocation = True

@repeatEvery(seconds=config['youtube']['repeatInterval'])
async def fetchAndUpdateYoutubeData():
    try:
        print('Starting fetchAndUpdateYoutubeData')
        global isFirstInvocation

        # during the first invocation, we will fetch videos that are atmost 100 days older, but during subsequent invocations, we will only fetch videos which are only an hour older
        timeDelta = datetime.timedelta(days=100) if isFirstInvocation else datetime.timedelta(minutes=60)
        
        # during the first invocation we will fetch more videos, because we have to cover more range of time, in the subsequent runs, videos will start repeating so it's ok to fetch less number of latest videos'
        numVideos = config['youtube']['videosLimitFirstTime'] if isFirstInvocation else config['youtube']['videosLimitSubsequentTime']

        isFirstInvocation = False

        params = {
            'key': os.environ['YOUTUBE_API_KEY'],
            'q': config['youtube']['query'],
            'type': 'video',
            'order': 'date',
            'part': 'snippet',
            'maxResults': 50,
            # fetching the videos for last 30 minutes
            'publishedAfter': (datetime.datetime.utcnow() - timeDelta).strftime('%Y-%m-%dT%H:%M:%SZ')
        }

        videos = await fetchYoutubeVideos(lim=numVideos, params=params)

        
        with sessionManager() as session:

            # calculating already present video_ids
            res = session.query(Video.video_id).filter(Video.video_id.in_([video['video_id'] for video in videos]))
            presentVideoIds = [r.video_id for r in res]

            insertableVideos = list(filter(lambda x: x['video_id'] not in presentVideoIds, videos))
            print(f'Inserted {len(insertableVideos)} videos to the db\n')

            # using bulk insert instead of orms session.add_all for speed
            session.bulk_insert_mappings(Video, insertableVideos)
            session.commit()
    except Exception:
        print('Error in fetchAndUpdateYoutubeData job')
        print(traceback.format_exc())

    


if __name__=='__main__':
    asyncio.run(fetchAndUpdateYoutubeData())