# Pieces Demo

## Usage
If you want to save time please do not worry about installing and just run:
```bash
docker pull odellus052/pieces-demo:v0.0.3
docker run -v $(pwd)/out:/app/out odellus052/pieces-demo:v0.0.3 python sql_agent.py
```
Answers appear in `out/answers.jsonl` and look like this
```json
{"patient_id": "p1", "question": "Did patient p1 have Hypertension/Hypotension given blood-pressure records from vitals?", "answer": "Yes, patient p1 had Hypertension given the blood pressure record of 186/82 mmHg from the vitals."}
{"patient_id": "p1", "question": "Did patient p1 get the medication order to treat hypertension/hypotension if any?", "answer": "Yes, patient p1 received a medication order for LABETALOL, which is used to treat hypertension, with the instruction to administer if Systolic BP is greater than 160 mmHg."}
{"patient_id": "p2", "question": "Did patient p2 have Hypertension/Hypotension given blood-pressure records from vitals?", "answer": "Yes, patient p2 had Hypotension given the blood pressure record of 68/41 mmHg."}
{"patient_id": "p2", "question": "Did patient p2 get the medication order to treat hypertension/hypotension if any?", "answer": "No, patient p2 did not get the medication order to treat hypertension/hypotension if any."}
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
