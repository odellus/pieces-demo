# Pieces Demo

## Problem


## Usage
If you want to save time please do not worry about installing and just run:
```bash
mkdir out
docker pull odellus052/pieces-demo:v0.0.7
docker run -v $(pwd)/out:/app/out odellus052/pieces-demo:v0.0.7 python sql_agent.py
```


## Install
### Local
To run the script outside of a docker container execute the following steps:
```bash
conda create -n pieces-demo pip python=3.11
python -m pip install requirements.txt
python sql_agent.py
```
### Docker
To build your own docker container do the following
```bash
export IMAGE_TAG=vX.XX.XXX
export DOCKER_USER=#your docker username
# login to docker to push
docker login
bash build_image.sh
docker run -v $(pwd)/out:/app/out ${DOCKER_USER}/pieces-demo:${IMAGE_TAG} python sql_agent.py
```


## Mad lib
I put together a solution that is more reliable than having GPT-4 generate SQL queries on the fly by picking good queries that got the correct answer and putting them into a pipeline to answer the questions with no machine learning. To run simply do
```bash
sudo docker run -v $(pwd)/out:/app/out odellus052/pieces-demo:v0.0.7 python mad_lib.py
```
Which will write to `stdout`
```
Patient p1 has hypertension: True
Patient p1 has hypotension: False
Patient p1 has taken blood pressure drugs: True
---
Patient p2 has hypertension: False
Patient p2 has hypotension: True
Patient p2 has taken blood pressure drugs: False
---
```