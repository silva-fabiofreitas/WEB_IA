from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from decouple import config
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import pandas as pd
from ..state import GraphState
from ...sql_agent import get_engine


def execute_query(state: GraphState) -> GraphState:
    """
    Executes a query based on the provided state.
    Args:
        state (GraphState): A dictionary containing the following

    """
    print('--EXCECUTAR QUERY INICIADO--')
    engine = get_engine()
    try:
        db = SQLDatabase(engine=engine)
        data = db.run(state['query'])
    finally:
        engine.dispose()

    return {"chart_data": data}