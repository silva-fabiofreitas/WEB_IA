from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class MindMap:
    def __init__(self,question):
        self.question = question


    def invoke(self):
        llm = ChatOpenAI()
        chain = self.prompt | llm | self.output_parser
        return chain.invoke({"input": self.question })


    @property
    def template(self):
        return """
        Você é um especialista jurídico e professor de direito no Brasil.
        Elabora mapas mentais envolventes e informativos que destacam conexões, tendências e insights de maneira visualmente atraente. 
        Seu projeto atual envolve a criação de uma visualização de mapa mental relacionados a disciplina de direto, para ajudar os estudantes de direito a memorizar o conteudo e passar na prova da OAB.
        Aproveitando suas habilidades em design gráfico, você criará um mapa mental que não apenas simplifica a informação, mas também a torna mais acessível e atraente.
        Decida a estrutura do mapa mental, como representar visualmente a hierarquia, as conexões e as relações do conjunto de dados. Isso inclui determinar o nó central, sub-nós e como eles serão interconectados
       
        question:{input}
        Formate a saida em markdown 
        """

    @property
    def prompt(self):
        return ChatPromptTemplate.from_template(template= self.template)
    
    @property
    def output_parser(self):
        return StrOutputParser()

