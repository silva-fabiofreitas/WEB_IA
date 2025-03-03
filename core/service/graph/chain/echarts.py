from .llm import model
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate


class ChartOptions(BaseModel):
    """ECharts options."""
    options: str =  Field(..., description="Echarts options, json.") 


def get_chain_echarts_options():
    llm = model()
    template = """"Voce e um especialista na biblioteca javascript echarts.
    Com base no tipo de grafico fornecido {chart_type}, crie um grafico que melhor represente os resultados.
    Resultados: {data}

    Reposta deve ser um options do echarts formate a saide em json.

    """

    prompt_chart_desing = PromptTemplate.from_template(template)

    llm_with_struct_echart = llm.with_structured_output(ChartOptions)
    return prompt_chart_desing | llm_with_struct_echart