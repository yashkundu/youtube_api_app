from config import config
from utils.decorators import repeatEvery
import httpx
import os
import datetime
from utils.general import recDictKeyFetcher


# This field is used the identify if the scheduled job is invoked first time or not
isFirstInvocation = True
youtubeSearchUrl = 'https://www.googleapis.com/youtube/v3/search'


# TODO check response status, and also if out quota is exhausted
async def fetchYoutubeVideos(lim: int, params: dict) -> list[dict]:
    cnt = 0
    nextPageToken = None
    data = []
    firstIter = True
    while firstIter or (cnt<lim and nextPageToken):
        firstIter = False
        async with httpx.AsyncClient() as client:
            newParams = {**params}
            if nextPageToken:
                newParams['pageToken'] = nextPageToken
            r = await client.get(youtubeSearchUrl, params=params)
            d = r.json()
            cnt += d['pageInfo']['resultsPerPage']
            nextPageToken = d.get('nextPageToken', None)
            data.extend(map(lambda x: {
                'publishedAt': recDictKeyFetcher(x, 'snippet', 'publishedAt')
            }, d.get('items', [])))


# @repeatEvery(seconds=config['youtube']['repeatInterval'])
async def fetchYoutubeData():

    params = {
        'key': os.environ['YOUTUBE_API_KEY'],
        'q': config['youtube']['query'],
        'type': 'video',
        'order': 'date',
        'part': 'snippet',
        'maxResults': 50,
        # fetching the videos for last 30 minutes
        'publishedAfter': (datetime.datetime.utcnow() - datetime.timedelta(minutes=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
    }
    async with httpx.AsyncClient as client:
        r = await client.get('https://www.googleapis.com/youtube/v3/search')