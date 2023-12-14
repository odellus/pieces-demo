import json
import yaml
import pandas as pd
from sqlalchemy import create_engine
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.chat_models.openai import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType


def get_cfg():
    '''Load the config file'''
    with open("config.yaml", 'r') as f:
        return yaml.load(f, Loader=yaml.Loader)


def get_prefix(dialect, top_k):
    return f'''You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
Definition of Hypotension: Hypotension (low blood pressure) is generally considered a blood pressure reading lower than 90 mmHg for the top number (systolic) or 60 mm Hg for the bottom number (diastolic).
Definition of Hypertension: Hypertension (high blood pressure) is when the pressure in your blood vessels is too high (140/90 mmHg or higher).
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
If the query comes back as empty, return "No" as the answer.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return "I don\'t know" as the answer.
'''


def load_data(cfg):
    '''Load the data from CSV files into the database'''
    engine = create_engine(cfg['POSTGRES_URI'])
    df = pd.read_csv('./interview dataset - medication.csv')
    df.columns = [c.lower() for c in df.columns]
    df.to_sql('medication', engine, if_exists='replace', index=False)
    df = pd.read_csv('./interview dataset - vital.csv')
    df.columns = [c.lower() for c in df.columns]
    df.to_sql('vitals', engine, if_exists='replace', index=False)

def get_db(cfg):
    '''Create a SQLDatabase object'''
    postgres_uri = cfg['POSTGRES_URI']
    db = SQLDatabase.from_uri(postgres_uri)
    return db


def get_llm(cfg):
    '''Create a language model'''
    llm = ChatOpenAI(
        temperature = 0.0,
        model_name = 'gpt-4-1106-preview',
        openai_api_key=cfg['OPENAI_API_KEY'],
    )
    return llm


def get_questions(patient_id):
    '''Get a list of questions to ask for a given patient'''
    return [
        f'Did patient {patient_id} have Hypertension/Hypotension given blood-pressure records from vitals?',
        f'Did patient {patient_id} get the medication order to treat hypertension/hypotension if any?',
    ]


def get_patient_ids():
    '''Get a list of patient IDs to ask questions about'''
    return ['p1', 'p2']


def get_agent(cfg, verbose = True):
    '''Create an agent'''
    db = get_db(cfg)
    llm = get_llm(cfg)
    prefix = get_prefix(db.dialect, 5)
    toolkit = SQLDatabaseToolkit(db = db, llm = llm)
    agent = create_sql_agent(
        llm = llm,
        toolkit = toolkit,
        agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        prefix = prefix,
        verbose = verbose,
    )
    return agent


def ask_questions():
    '''Ask questions'''
    # We keep our secrets in a YAML config file
    cfg = get_cfg()
    # Load the data from CSV files into the database
    load_data(cfg)
    # Create the agent
    agent = get_agent(cfg)
    # Ask questions
    patient_ids = get_patient_ids()
    final_answers = []
    for patient_id in patient_ids:
        questions = get_questions(patient_id)
        for question in questions:
            print(question)
            answer = agent.run(question)
            print(answer)
            d = dict(
                patient_id = patient_id,
                question = question,
                answer = answer,
            )
            final_answers.append(d)
            with open('out/answers.jsonl', 'a') as f:
                f.write(json.dumps(d) + '\n')

    print('Final answers:')
    for d in final_answers:
        print(d)

if __name__ == '__main__':
    ask_questions()