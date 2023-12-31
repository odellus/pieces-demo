# Analysis and Methodology
### Overview
The project entailed developing a system to analyze patient data, focusing on hypertension and hypotension indicators and related medication orders. The data was derived from two primary sources: vitals and medication records. We seek to answer two questions:
- Did the patient have Hypertension/Hypotension given blood-pressure records from vitals?
- Did the patient get the medication order to treat hypertension/hypotension if any?
# Data Sources
### Vitals

The vitals table was structured in SQL to include patient ID, the type of measurement, the date of observation, the result, and the units of measurement. This table was crucial for assessing blood pressure records.
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
p1      Pulse   2023-12-04 21:21:00     77      None
*/
```
### Medication

The medication table encompassed patient ID, medication interval, start date of the order, medication description, amount, units, form, and provider instructions. This table was essential for evaluating medication orders related to blood pressure conditions.
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

# Development Tools and Resources

- [Langchain SQL Agent](https://python.langchain.com/docs/integrations/toolkits/sql_database): Initially employed for its efficacy and ease of integration.
- Development Environment: Visual Studio Code.
- Assistance Tools: Utilized ChatGPT for specific Docker-related queries and GitHub Copilot for generating function docstrings.
- Database Hosting: Employed a free tier PostgreSQL database from [ElephantSQL](https://elephantsql.com/).

# Approach
### Initial Steps

The process began with a focus on ensuring accurate SQL query formulation, particularly for PostgreSQL syntax. Modifications were made to the get_prefix function of the langchain SQL agent. Key steps included:

- Lowercasing column names in the database to simplify query construction.
- Integrating definitions for hypotension and hypertension into the SQL agent's prefix for more precise query formulation.
- Adjusting the interpretation of empty query results to differentiate between errors and negative outcomes.

## Further Refinements

Subsequent modifications involved:

- Renaming input CSV files for seamless integration into the Docker environment.
- Implementing logging mechanisms to track queries, results, and final answers.
- Enhancing query accuracy by incorporating specific search patterns in provider instructions.

# Results Analysis
### Initial Results

The system initially produced accurate assessments for the first question regarding hypertension/hypotension but encountered difficulties with the second question, related to medication orders.

### Enhanced Results

With refinements, the system showed improved capability in identifying relevant medications and correctly interpreting blood pressure data.

### Results
```python
{'patient_id': 'p1', 'question': 'Did patient p1 have Hypertension/Hypotension given blood-pressure records from vitals?', 'answer': 'Yes, patient p1 had Hypertension.', 'sql_query': "SELECT observationresult FROM vitals WHERE patientid = 'p1' AND componentid = 'BloodPressure' ORDER BY observationdate DESC LIMIT 5", 'sql_result': "[('186/82',)]", 'timestamp': '2023-12-14 16:37:26'}
{'patient_id': 'p1', 'question': 'Did patient p1 get the medication order to treat hypertension/hypotension if any?', 'answer': "Yes, patient p1 has been given the medication 'LABETALOL 20 MG/4 ML (5 MG/ML) INTRAVENOUS SYRINGE' to treat hypertension.", 'sql_query': "SELECT description, providerinstructions FROM medication WHERE patientid = 'p1' AND (providerinstructions LIKE '%BP GREATER%' OR providerinstructions LIKE '%BP LESS%') LIMIT 5;", 'sql_result': "[('LABETALOL 20 MG/4 ML (5 MG/ML) INTRAVENOUS SYRINGE', 'Administer if Systolic BP GREATER than 160')]", 'timestamp': '2023-12-14 16:38:07'}
{'patient_id': 'p2', 'question': 'Did patient p2 have Hypertension/Hypotension given blood-pressure records from vitals?', 'answer': 'Yes, patient p2 had Hypotension.', 'sql_query': "SELECT observationresult FROM vitals WHERE patientid = 'p2' AND componentid = 'BloodPressure' ORDER BY observationdate DESC LIMIT 5", 'sql_result': "[('68/41',), ('108/63',)]", 'timestamp': '2023-12-14 16:38:42'}
{'patient_id': 'p2', 'question': 'Did patient p2 get the medication order to treat hypertension/hypotension if any?', 'answer': 'No', 'sql_query': "SELECT patientid, orderstartdate, description, providerinstructions FROM medication WHERE patientid = 'p2' AND providerinstructions LIKE '%BP%' ORDER BY orderstartdate DESC LIMIT 5", 'sql_result': '', 'timestamp': '2023-12-14 16:39:13'}
```

# Discussion

The findings suggest that a chatbot-like interface may not be essential for regular query execution. The potential for a template-based approach could offer a more cost-effective and reliable alternative. The successful application of Text2SQL agents in generating accurate queries highlights the feasibility of a non-machine learning based solution for similar tasks.

# Conclusion

The project demonstrated the capability of a Text2SQL agent in effectively handling specific medical queries. The transition to a non-machine learning approach for query execution and response formulation was successfully tested, indicating a scalable and efficient solution for similar data analysis tasks. The final Python script exemplifies this approach, showcasing the practical application of the developed methodology.

