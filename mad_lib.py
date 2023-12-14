from sqlalchemy import create_engine, text
from sql_agent import get_cfg

def get_bp_drugs_qry(patient_id, limit = 5):
    return f"""SELECT description, providerinstructions FROM medication WHERE patientid = '{patient_id}' AND providerinstructions LIKE '%BP%' LIMIT {limit}"""

def get_vitals_qry(patient_id, limit = 5):
    return f"""SELECT observationresult FROM vitals WHERE patientid = 'p1' AND componentid = 'BloodPressure' ORDER BY observationdate DESC LIMIT {limit}"""