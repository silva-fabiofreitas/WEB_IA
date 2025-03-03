from ..state import GraphState
from ..chain.write_query import get_structured_llm


def write_query(state: GraphState) -> GraphState:
    """
    Generates a query based on the provided state using a structured language model.
    Args:
        state (GraphState): A dictionary containing the following keys:
            - "question" (str): The input question to generate the query for.
            - "dialect" (str): The SQL dialect to use for the query.
            - "top_k" (int): The number of top results to consider.
            - "table_info" (dict): Information about the table structure.
    Returns:
        GraphState: A dictionary containing the generated query with the key "query".
    """
    print('--GERAR QUERY INICIADO--')

    llm = get_structured_llm()

    query = llm.invoke({
        'input':state["question"],
        'dialect': state["dialect"],
        'top_k': state["top_k"],
        'table_info': state['table_info']
        })
    
    return {"query": query['query']}
