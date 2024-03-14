


## How to run
Edit the docker-compose.yml file, 
in the environment section:
```yaml
environment:
      - YOUTUBE_API_KEY=*
```
Replace * with a google api key.

Run the application with docker compose:
```shell
docker compose up
```

## Framework used
Python's Fastapi with asyncio



## Unhandled things
The exhaustion of api keys is not handled in this implementation.


## Additional info
migration/base.sql contains the initialization script which creates the required tables and index for mysql database.

Sometimes while running the setup on local computer, I noticed that the app service in docker gets less cpu cycles, due to which the job which executes in regular intervals to fetch youtube video gets delayed by a few seconds, but most of the times it works fine.
