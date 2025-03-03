from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from .llm import model


class ChartSuggestion(BaseModel):
    """Sugest chart type."""
    chart_type: list[str] = Field(..., description="Type of chart to suggest.")


def get_chain_chart_choice():
    llm = model()

    template = """Com base na amostra de dados fornecida {data}, analise as variáveis e sugira o tipo de gráfico que melhor representa os resultados. Considere os seguintes pontos:
    1. **Tipo de Dados:** Identifique se os dados são categóricos, numéricos, temporais ou relacionais.
    2. **Objetivo da Visualização:** Determine se o objetivo é comparar valores, mostrar distribuições, evidenciar tendências, ou destacar relações entre variáveis.
    3. **Sugestão de Gráfico:** Recomende o gráfico mais adequado (ex: gráfico de barras, linhas, dispersão, pizza, histograma, boxplot, etc.) com base na natureza dos dados e no objetivo.
    4. **Consideração do Usuário:** Se o usuário especificar um tipo de gráfico na pergunta {question}, priorize a sugestão do usuário, mas avalie se é adequado para os dados fornecidos. Caso não seja, explique brevemente por que outro gráfico seria mais eficaz.
    """

    prompt_chart_type = PromptTemplate.from_template(template)
    llm_with_struct_chart = llm.with_structured_output(ChartSuggestion)
    return prompt_chart_type | llm_with_struct_chart