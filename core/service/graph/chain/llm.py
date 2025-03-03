from langchain_openai import ChatOpenAI


def model(model="gpt-4o-mini", max_tokens=512):
    return ChatOpenAI(
        model=model,
        temperature=0,
        max_tokens=max_tokens,  # Limita o tamanho da resposta (evita SQL truncado)
        model_kwargs={
            'frequency_penalty': 0,
            'presence_penalty': 0,
            'top_p': 0.1 # Foca nos tokens mais relevantes
        }
    )