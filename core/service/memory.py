from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, MarkdownListOutputParser
from langchain_core.messages import HumanMessage, trim_messages
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import ConfigurableFieldSpec

from decouple import config


import uuid

from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_postgres import PostgresChatMessageHistory
import psycopg

import uuid

def generate_custom_uuid(username: str) -> uuid.UUID:
    """Gera um uuid personalidado com o nome do usuario 

    Args:
        username (str): nome do usuario concatenado com seu id

    Returns:
        uuid.UUID: _description_
    """    
    # Usamos um namespace predefinido. O namespace DNS é comumente usado, mas você pode definir o seu próprio.
    namespace = uuid.NAMESPACE_DNS
    # Geramos o UUIDv5 baseado no namespace e no nome de usuário.
    custom_uuid = uuid.uuid5(namespace, username).__str__()
    
    return custom_uuid


class SessionHistoryDatabase:
    def __init__(self, uri=None, table_name="chat_history"):
        self.uri = uri
        self.table_name = table_name

    def db_connection(self):
        """Estabelece uma conexão sincrona com o banco de dados
        # (or use psycopg.AsyncConnection for async)

        Returns:
            class: django.db.backends.postgresql.base.DatabaseWrapper
        """
        
        POSTGRES_NAME = config('POSTGRES_NAME')
        POSTGRES_USER = config('POSTGRES_USER')
        POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
        POSTGRES_HOST = config('POSTGRES_HOST')
        POSTGRES_PORT = config('POSTGRES_PORT')
        
        if not self.uri:
            return psycopg.connect(
                f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"
            )
            
        return psycopg.connect(self.uri)

    def creat_history_table(self):
        """Criar tabela para armazenar o historico de conversas, executar apenas uma vez
        """
        PostgresChatMessageHistory.create_tables(self.db_connection(), self.table_name)

    def get_session_history(self, session_id):
        return PostgresChatMessageHistory(
            self.table_name, session_id, sync_connection=self.db_connection()
        )


class ChatHistory(SessionHistoryDatabase):
    
    def stream(self, input, session_id):
        return self.runnable_with_history.stream(
            [HumanMessage(content=input)],
            config={
                "configurable": {
                    "session_id": session_id,
                }
            },
        )
    
    @property
    def runnable_with_history(self):
        return RunnableWithMessageHistory(
            self.trimm | self.llm | StrOutputParser(),
            self.get_session_history,
        )
        
    @property    
    def llm(self):
        return ChatOpenAI(model="gpt-4o-mini")
    
    @property
    def trimm(self):
        return trim_messages(
        max_tokens=400,
        strategy="last",
        token_counter=self.llm,
        include_system=True,
        allow_partial=False,
        start_on="human",
        )
    