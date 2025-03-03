from langchain_core.prompts import PromptTemplate
from typing_extensions import Annotated
from .llm import model
from pydantic import BaseModel, Field


class QueryOutput(BaseModel):
    """Generated SQL query."""
    query: Annotated[str, Field(..., description="Syntactically valid SQL query.")]


def get_structured_llm():
    llm = model()

    template_sql = """Given an input question, create a syntactically correct {dialect} query to run to help find the answer. Unless the user specifies in his question a specific number of examples they wish to obtain, always limit your query to at most {top_k} results. You can order the results by a relevant column to return the most interesting examples in the database.

    Never query for all the columns from a specific table; only ask for the few relevant columns given the question.

    Pay attention to use only the column names that you can see in the schema description. Be careful not to query for columns that do not exist. Also, pay attention to which column is in which table.

    use only the following tables:
    {table_info}

    Question: {input}
    """

    prompt = PromptTemplate.from_template(
        template_sql,
    )

    llm_with_struct = prompt | llm.with_structured_output(QueryOutput)

    return llm_with_struct
