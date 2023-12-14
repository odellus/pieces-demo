import pandas as pd
from sqlalchemy import create_engine, text
from sql_agent import get_cfg

def get_bp_drugs_qry(patient_id, limit = 5):
    qry = f"""SELECT description, providerinstructions FROM medication WHERE patientid = '{patient_id}' AND providerinstructions LIKE '%BP%' LIMIT {limit}"""
    return text(qry)

def get_vitals_qry(patient_id, limit = 5):
    qry = f"""SELECT observationresult FROM vitals WHERE patientid = '{patient_id}' AND componentid = 'BloodPressure' ORDER BY observationdate DESC LIMIT {limit}"""
    return text(qry)

def check_patient_vitals(patient_id, engine):
    '''Check if a patient has any vitals'''
    qry = get_vitals_qry(patient_id)
    df = pd.read_sql(qry, engine)
    dfout = df.observationresult.str.split('/', expand=True)
    dfout.columns = ['systolic', 'diastolic']
    dfout = dfout.astype(float)
    dfout['hypertension'] = dfout.systolic >= 140
    dfout['hypotension'] = dfout.diastolic <= 60
    return {
        'hypertension': dfout.hypertension.any(), 
        'hypotension': dfout.hypotension.any()
    }

def check_patient_drugs(patient_id, engine):
    '''Check if a patient has any drugs'''
    qry = get_bp_drugs_qry(patient_id)
    df = pd.read_sql(qry, engine)
    return df.shape[0] > 0

def no_ml():
    patient_ids = ['p1', 'p2']
    cfg = get_cfg()
    engine = create_engine(cfg['POSTGRES_URI'])
    for patient_id in patient_ids:
        has_vitals = check_patient_vitals(patient_id, engine)
        has_drugs = check_patient_drugs(patient_id, engine)
        print(f'Patient {patient_id} has hypertension: {has_vitals["hypertension"]}')
        print(f'Patient {patient_id} has hypotension: {has_vitals["hypotension"]}')
        print(f'Patient {patient_id} has taken blood pressure drugs: {has_drugs}')
        print('---')

if __name__ == '__main__':
    no_ml()