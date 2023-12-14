# Results

## Questions
- Did the patient have Hypertension/Hypotension given blood-pressure records from vitals?
- Did the patient get the medication order to treat hypertension/hypotension if any?

## Data
### vitals
```sql
CREATE TABLE vitals (
        patientid TEXT, 
        componentid TEXT, 
        observationdate TEXT, 
        observationresult TEXT, 
        observationunits TEXT
)

/*
3 rows from vitals table:
patientid       componentid     observationdate observationresult       observationunits
p1      BloodPressure   2023-12-04 21:21:00     186/82  mmHg
p1      Temp    2023-12-04 21:21:00     97.5    F
p1      Pulse   2023-12-04 21:21:00     77      None```
```
### medication
```sql
CREATE TABLE medication (
        patientid TEXT, 
        medinterval TEXT, 
        orderstartdate TEXT, 
        description TEXT, 
        amount BIGINT, 
        units TEXT, 
        dosageform TEXT, 
        providerinstructions TEXT
)

/*
3 rows from medication table:
patientid       medinterval     orderstartdate  description     amount  units   dosageform      providerinstructions
p1      Once 1700       2023-12-04 23:00:00     MORPHINE 4 MG/ML INJECTION SYRINGE WRAPPER      4       mg      IV      StatIf both oral and IV options are ordered for same pain level, administer IV if patient not able t
p1      Once 1700       2023-12-04 23:00:00     LABETALOL 20 MG/4 ML (5 MG/ML) INTRAVENOUS SYRINGE      10      mg      IV      Administer if Systolic BP GREATER than 160
p1      Once 1745       2023-12-04 23:45:00     POTASSIUM CHLORIDE ER 20 MEQ TABLET,EXTENDED RELEASE(PART/CRYST)        40      mEq     oral      Do not crush, split, or chew.
*/
```



# Tools

I decide to start with the default [langchain sql agent](https://python.langchain.com/docs/integrations/toolkits/sql_database) as it usually gives good results and is fast to implement as a first try.

I used VS Code for the coding. I asked chatgpt one question about how to pass in the volume to docker run because I couldn't remember whether it's `-v host:container` or `-v container:host` (it's the former). I used Github Copilot to write the function docstrings inside [sql_agent.py](./sql_agent.py). I'm pretty sure I tabbed through to autocomplete some of the code as well. Especially the final part. Once you get all of your functions defined it's pretty obvious how you want to use them most of the time.


I used a free tier postgresql database from [ElephantSQL](https://elephantsql.com) to store our medication and vitals tables.

The minor modifications I made to the default langchain sql agent were mostly in the fuction `get_prefix` and are noted under [Approach](#approach).

# Approach
Initially the results were good for the first question for both patients, but it failed on the second question and struggled with getting the right syntax for postgresql. So in the loading step I lowercased all of the columns names for postgres, simplifying our task for our agent.

I included the given definitions for hypotension and hypertension into the prefix of the sql agent so that it would be able to construct better queries for finding medications that are administered to treat blood pressue for the second question. With the addition of this information the sql agent was able to successfully find the medication administered for hypertension for patient p1. 

However, it was failing for patient p2 because it assumed an empty result meant there had been some error.

The last piece of the puzzle was including into the prefix the line:
```
If the query comes back as empty, return "No" as the answer.
```
This allowed our agent to conclude that null results from running its query were not actually an error in query construction, but a negative result. In this case we must answer the question of whether a drug was administered as "No."

Finally I changed the names of the input CSV files to get rid of the spaces because I could not figure out how to `COPY` them over with the spaces in the files names in the [Dockerfile](./Dockerfile).


# Results
The results of asking the questions
```json
{"patient_id": "p1", "question": "Did patient p1 have Hypertension/Hypotension given blood-pressure records from vitals?", "answer": "Yes, patient p1 had Hypertension given the blood pressure record of 186/82 mmHg."}
{"patient_id": "p1", "question": "Did patient p1 get the medication order to treat hypertension/hypotension if any?", "answer": "Yes, patient p1 did receive a medication order for treating hypertension. The medication prescribed was LABETALOL, with instructions to administer if the systolic blood pressure is greater than 160 mmHg."}
{"patient_id": "p2", "question": "Did patient p2 have Hypertension/Hypotension given blood-pressure records from vitals?", "answer": "Patient p2 had hypotension based on a blood pressure reading of 68/41 mmHg. Another reading of 108/63 mmHg was within the normal range."}
{"patient_id": "p2", "question": "Did patient p2 get the medication order to treat hypertension/hypotension if any?", "answer": "No, patient p2 did not get a medication order to treat hypertension/hypotension."}
```

# Discussion
We would not necessarily need a chatbot like interface to turn these results into a product if these are common questions we wish to populate regularly. The queries our agent created on the fly to answer these questions could be saved and re-used in the future. Furthermore there is a good possibility that we could use a madlib, template-based approach to create human-like answers from the results of our queries, thus removing any need for an LLM at all and lowering costs.

I added logging so we could keep track of which questions were asked, which queries were run, and the results of those queries in addition to the question and final answer. I decide to go ahead and add them into what we're writing to `answers.jsonl`
```json
{'patient_id': 'p1', 'question': 'Did patient p1 have Hypertension/Hypotension given blood-pressure records from vitals?', 'answer': 'Yes, patient p1 had Hypertension.', 'sql_query': "SELECT observationresult FROM vitals WHERE patientid = 'p1' AND componentid = 'BloodPressure' LIMIT 5", 'sql_result': "[('186/82',)]", 'timestamp': '2023-12-14 20:52:14'}
{'patient_id': 'p1', 'question': 'Did patient p1 get the medication order to treat hypertension/hypotension if any?', 'answer': 'No', 'sql_query': "SELECT description, providerinstructions FROM medication WHERE patientid = 'p1' AND (providerinstructions LIKE '%hypertension%' OR providerinstructions LIKE '%hypotension%' OR description LIKE '%hypertension%' OR description LIKE '%hypotension%') LIMIT 5;", 'sql_result': '', 'timestamp': '2023-12-14 20:52:43'}
{'patient_id': 'p2', 'question': 'Did patient p2 have Hypertension/Hypotension given blood-pressure records from vitals?', 'answer': "Yes, patient p2 had hypotension on '2023-11-29 12:52:00'.", 'sql_query': "SELECT observationdate, observationresult FROM vitals WHERE patientid = 'p2' AND componentid = 'BloodPressure' ORDER BY observationdate DESC LIMIT 5;", 'sql_result': "[('2023-11-29 12:52:00', '68/41'), ('2023-11-29 12:32:00', '108/63')]", 'timestamp': '2023-12-14 20:53:28'}
{'patient_id': 'p2', 'question': 'Did patient p2 get the medication order to treat hypertension/hypotension if any?', 'answer': 'No', 'sql_query': "SELECT description FROM medication WHERE patientid = 'p2' AND (description LIKE '%hypertension%' OR description LIKE '%hypotension%') LIMIT 5;", 'sql_result': '', 'timestamp': '2023-12-14 20:53:58'}
```
This allows us to reuse these queries in a separate system like what I am putting together in [mad_lib.py](./mad_lib.py)

# Conclusion
With a bit of prompt engineering we were able to construct a Text2SQL agent capable of answering the given questions based on the information contained in the provided tables.