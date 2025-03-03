from ..state import GraphState
from ..chain.choice_chart import get_chain_chart_choice


def choose_chart(state: GraphState) -> GraphState:
    """
    Choose the chart type based on the data provided.
    Args:
        state (GraphState): A dictionary containing the following

    """
    print('--CHOOSE CHART STARTED--')

    llm = get_chain_chart_choice()
    chart_type = llm.invoke({
        'question':state['question'],
        'data': state['chart_data'],
    })
    print(chart_type)

    return {'chart_type': chart_type['chart_type'][0]}