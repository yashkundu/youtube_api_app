FROM python:3.11-slim-bullseye

# Install pipenv and compilation dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
# Copy code 
COPY . ./app/
WORKDIR /app

EXPOSE 3000

ENTRYPOINT ["python3", "-m", "gunicorn", "-b", "0.0.0.0:3000", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-n", "2"]