from dotenv import load_dotenv

from langgraph.graph import StateGraph, END, START

from .node.choose_chart import choose_chart
from .node.execute_query import execute_query
from.node.write_query import write_query
from .node.generate_chart import generate_chart
from .state import GraphState

load_dotenv()

WRITE_QUERY = 'write query'
CHOOSE_CHART = 'choose chart' 
EXECUTE_QUERY = 'execute query'
GENERATE_CHART = 'generate chart'   


graph_builder = StateGraph(GraphState)

graph_builder.add_node(WRITE_QUERY, write_query)
graph_builder.add_node(EXECUTE_QUERY, execute_query)
graph_builder.add_node(CHOOSE_CHART, choose_chart)
graph_builder.add_node(GENERATE_CHART, generate_chart)

graph_builder.add_edge(START, WRITE_QUERY)
graph_builder.add_edge(WRITE_QUERY, EXECUTE_QUERY)
graph_builder.add_edge(EXECUTE_QUERY, CHOOSE_CHART)
graph_builder.add_edge(CHOOSE_CHART, GENERATE_CHART)
graph_builder.add_edge(GENERATE_CHART, END)

graph = graph_builder.compile()

# graph.get_graph().draw_mermaid_png(output_file_path='graph.png')
