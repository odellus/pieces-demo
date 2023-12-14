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

## Approach
Initially the results were good for the first question for both patients, but it failed on the second question and struggled with getting the right syntax for postgresql. So I changed it so in the loading step all of the columns in the postgres table would be lowercase, simplifying our task for our agent.

I also included the definitions for hypotension and hypertension into the prefix of the sql agent so that it would be able to construct better queries for finding medications that are administered to treat blood pressue for the second question. With the addition of this information it was able to successfully find the medication administered for hypertension for patient p1. However, it was failing for patient p2 because when it got back an empty result it assumed there had been some error.

The last piece of the puzzle was including into the prefix the line:
```
If the query comes back as empty, return "No" as the answer.
```
This allowed our agent to conclude that null results from running its query were not actually an error in query construction, but a possible result to which we must answer the question of whether a drug was administered as "No."

## Final results
```json
{"patient_id": "p1", "question": "Did patient p1 have Hypertension/Hypotension given blood-pressure records from vitals?", "answer": "Yes, patient p1 had Hypertension given the blood pressure record of 186/82 mmHg."}
{"patient_id": "p1", "question": "Did patient p1 get the medication order to treat hypertension/hypotension if any?", "answer": "Yes, patient p1 did receive a medication order for treating hypertension. The medication prescribed was LABETALOL, with instructions to administer if the systolic blood pressure is greater than 160 mmHg."}
{"patient_id": "p2", "question": "Did patient p2 have Hypertension/Hypotension given blood-pressure records from vitals?", "answer": "Patient p2 had hypotension based on a blood pressure reading of 68/41 mmHg. Another reading of 108/63 mmHg was within the normal range."}
{"patient_id": "p2", "question": "Did patient p2 get the medication order to treat hypertension/hypotension if any?", "answer": "No, patient p2 did not get a medication order to treat hypertension/hypotension."}
```