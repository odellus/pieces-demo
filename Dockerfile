FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

RUN mkdir out

COPY ./config.yaml ./sql_agent.py ./interview_dataset-medication.csv ./interview_dataset-vital.csv ./mad_lib.py /app/
