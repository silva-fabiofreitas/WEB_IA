from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class MindMap:
    def __init__(self, question):
        self.question = question

    def invoke(self):
        llm = OpenAI(temperature=0.1)
        chain = self.prompt | llm | self.output_parser
        return chain.invoke({"input": self.question})

    def chat(self, chat_history):
        llm = ChatOpenAI()
        chain = self.prompt | llm | self.output_parser
        response = chain.invoke({"input": self.question, "chat_history": chat_history})
        return response

    @property
    def prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                ("system", "Você é um professor de direito no Brasil."),
                ("system", "Elabora mapas mentais envolventes e informativos que destacam conexões, tendências e insights de maneira visualmente atraente."),
                ("assistant", "Decida a estrutura do mapa mental, como representar visualmente a hierarquia em diferentes niveis conforme as conexões e as relações do conjunto de dados"),
                ("human", "{input}"),
                ("placeholder", "{chat_history}"),
                ("ai", "Formate a saída em markdown"),
            ]
        )

    @property
    def output_parser(self):
        return StrOutputParser()
    
    
class ChatBot(MindMap):
    
    def chat(self, chat_history):
        llm = ChatOpenAI()
        chain = self.prompt | llm | self.output_parser
        response = chain.stream({"input": self.question, "chat_history": chat_history})
        return response
    
    @property
    def prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                ("system", "Voce é uma assitente virtual que tem conversas amigaveis sobre qualquer tema."),
                ("human", "{input}"),
                ("placeholder", "{chat_history}"),
                ("ai", "Reponda de maneira cordial e amigavel"),
            ]
        )
    