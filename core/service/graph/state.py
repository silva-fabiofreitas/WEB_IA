from typing import TypedDict, List, Any


class GraphState(TypedDict):
    question: str
    chart_type: str
    chart_data: List[Any]
    dialect: str
    top_k: int = 10
    table_info: str
    query: str
    echart_options: dict