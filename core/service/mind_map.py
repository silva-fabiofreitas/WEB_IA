from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class MindMap:
    def __init__(self,answer):
        self.answer = answer


    def invoke(self):
        llm = ChatOpenAI()
        chain = self.prompt | llm | self.output_parser
        return chain.invoke({"input": self.answer })


    @property
    def template(self):
        return """
        Você é um especialista jurídico e professor de direito no Brasil
        Auxilia os alunos na criação de mapa mental (MindMap)
        O mapa mental deve conter a ideia principal, ramos e subramos, sempre apontar os artigos 
        Context:{input}
        Formate a saida do mapa mental em mardown 
        """

    @property
    def prompt(self):
        return ChatPromptTemplate.from_template(template= self.template)
    
    @property
    def output_parser(self):
        return StrOutputParser()

