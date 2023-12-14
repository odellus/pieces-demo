# Pieces Demo

## Usage
If you want to save time please do not worry about installing and just run:
```bash
docker pull odellus052/pieces-demo:v0.0.5
docker run -v $(pwd)/out:/app/out odellus052/pieces-demo:v0.0.5 python sql_agent.py
```
Answers appear in `out/answers.jsonl` and look like this
````python
{'patient_id': 'p1', 'question': 'Did patient p1 have Hypertension/Hypotension given blood-pressure records from vitals?', 'answer': 'Yes, patient p1 had Hypertension.', 'sql_query': "SELECT observationresult FROM vitals WHERE patientid = 'p1' AND componentid = 'BloodPressure' LIMIT 5", 'sql_result': "[('186/82',)]", 'timestamp': '2023-12-14 20:52:14'}
{'patient_id': 'p1', 'question': 'Did patient p1 get the medication order to treat hypertension/hypotension if any?', 'answer': 'No', 'sql_query': "SELECT description, providerinstructions FROM medication WHERE patientid = 'p1' AND (providerinstructions LIKE '%hypertension%' OR providerinstructions LIKE '%hypotension%' OR description LIKE '%hypertension%' OR description LIKE '%hypotension%') LIMIT 5;", 'sql_result': '', 'timestamp': '2023-12-14 20:52:43'}
{'patient_id': 'p2', 'question': 'Did patient p2 have Hypertension/Hypotension given blood-pressure records from vitals?', 'answer': "Yes, patient p2 had hypotension on '2023-11-29 12:52:00'.", 'sql_query': "SELECT observationdate, observationresult FROM vitals WHERE patientid = 'p2' AND componentid = 'BloodPressure' ORDER BY observationdate DESC LIMIT 5;", 'sql_result': "[('2023-11-29 12:52:00', '68/41'), ('2023-11-29 12:32:00', '108/63')]", 'timestamp': '2023-12-14 20:53:28'}
{'patient_id': 'p2', 'question': 'Did patient p2 get the medication order to treat hypertension/hypotension if any?', 'answer': 'No', 'sql_query': "SELECT description FROM medication WHERE patientid = 'p2' AND (description LIKE '%hypertension%' OR description LIKE '%hypotension%') LIMIT 5;", 'sql_result': '', 'timestamp': '2023-12-14 20:53:58'}
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
