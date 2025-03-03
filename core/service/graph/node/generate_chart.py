from ..state import GraphState
from ..chain.echarts import get_chain_echarts_options



def generate_chart(state: GraphState) -> GraphState:
    """
    Generate the chart based on the data provided.
    Args:
        state (GraphState): A dictionary containing the following

    """
    print('--GENERATE CHART STARTED--')

    llm = get_chain_echarts_options()
    echart_options = llm.invoke({
        'chart_type': state['chart_type'],
        'data': state['chart_data'],
    })

    return {'echart_options': echart_options}