from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from lifespan import lifespan


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def root():
    return {'message': 'Hello world'}