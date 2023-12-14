# Pieces Demo

## Usage
If you want to save time please do not worry about installing and just run:
```bash
docker pull odellus052/pieces-demo:v0.0.7
docker run -v $(pwd)/out:/app/out odellus052/pieces-demo:v0.0.7 python sql_agent.py
```
Answers appear in `out/answers.jsonl` and look like this without the extra newlines for easier reading
```python
{'answer': 'Yes, patient p1 had Hypertension.',
 'patient_id': 'p1',
 'question': 'Did patient p1 have Hypertension/Hypotension given '
             'blood-pressure records from vitals?',
 'sql_query': "SELECT observationresult FROM vitals WHERE patientid = 'p1' AND "
              "componentid = 'BloodPressure' ORDER BY observationdate DESC "
              'LIMIT 5',
 'sql_result': "[('186/82',)]",
 'timestamp': '2023-12-14 16:37:26'}

{'answer': "Yes, patient p1 has been given the medication 'LABETALOL 20 MG/4 "
           "ML (5 MG/ML) INTRAVENOUS SYRINGE' to treat hypertension.",
 'patient_id': 'p1',
 'question': 'Did patient p1 get the medication order to treat '
             'hypertension/hypotension if any?',
 'sql_query': 'SELECT description, providerinstructions FROM medication WHERE '
              "patientid = 'p1' AND (providerinstructions LIKE '%BP GREATER%' "
              "OR providerinstructions LIKE '%BP LESS%') LIMIT 5;",
 'sql_result': "[('LABETALOL 20 MG/4 ML (5 MG/ML) INTRAVENOUS SYRINGE', "
               "'Administer if Systolic BP GREATER than 160')]",
 'timestamp': '2023-12-14 16:38:07'}

'answer': 'Yes, patient p2 had Hypotension.',
 'patient_id': 'p2',
 'question': 'Did patient p2 have Hypertension/Hypotension given '
             'blood-pressure records from vitals?',
 'sql_query': "SELECT observationresult FROM vitals WHERE patientid = 'p2' AND "
              "componentid = 'BloodPressure' ORDER BY observationdate DESC "
              'LIMIT 5',
 'sql_result': "[('68/41',), ('108/63',)]",
 'timestamp': '2023-12-14 16:38:42'}

{'answer': 'No',
 'patient_id': 'p2',
 'question': 'Did patient p2 get the medication order to treat '
             'hypertension/hypotension if any?',
 'sql_query': 'SELECT patientid, orderstartdate, description, '
              "providerinstructions FROM medication WHERE patientid = 'p2' AND "
              "providerinstructions LIKE '%BP%' ORDER BY orderstartdate DESC "
              'LIMIT 5',
 'sql_result': '',
 'timestamp': '2023-12-14 16:39:13'}
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