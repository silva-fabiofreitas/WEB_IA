from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from decouple import config
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import pandas as pd
from ..state import GraphState


def execute_query(state: GraphState) -> GraphState:
    """
    Executes a query based on the provided state.
    Args:
        state (GraphState): A dictionary containing the following

    """
    print('--EXCECUTAR QUERY INICIADO--')
    POSTGRES_NAME = config('POSTGRES_NAME')
    POSTGRES_USER = config('POSTGRES_USER')
    POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
    POSTGRES_HOST = config('POSTGRES_HOST')
    POSTGRES_PORT = config('POSTGRES_PORT')
        
    DATABASE_URL = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"

    # Criando a engine do SQLAlchemy
    engine = create_engine(DATABASE_URL)

    db = SQLDatabase(engine=engine)
    data = db.run(state['query'])

    return {"chart_data": data}