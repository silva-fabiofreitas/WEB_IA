import time
import csv
from abc import ABC, abstractmethod

from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from decouple import config


class VectorStoreInterface(ABC):
    @abstractmethod
    def add_documents(self, documents: list[Document], ids: list[int]):
        pass


class PineconeVectorStoreService(VectorStoreInterface):
    """
    Classe responsável por gerenciar a conexão com o Pinecone.
    """
    def __init__(
        self, 
        api_key: str = None, 
        index_name: str = "text-to-sql", 
        dimension: int = 1536, 
        model: str = "text-embedding-3-small"
    ):
        self.pc = Pinecone(api_key= api_key or config('PINECONE_API_KEY'))
        self.index_name = index_name
        self.dimension = dimension
        self.embeddings = OpenAIEmbeddings(model=model)

        if not self._index_exists():
            self._create_index()

        self.vector_store = PineconeVectorStore(index=self.pc.Index(self.index_name), embedding=self.embeddings)

    
    def add_documents(self, documents: list[Document], ids:list[int]) -> list[str]:
        return self.vector_store.add_documents(documents=documents, ids=ids)
    
    def _index_exists(self) -> bool:
        existing_indexes = [index_info["name"] for index_info in self.pc.list_indexes()]
        return self.index_name in existing_indexes
    
    def _create_index(self) -> None:
        """
        Cria um novo índice no Pinecone, se não existir.
        """
        try:
            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

            timeout = 60  # Tempo máximo de espera (segundos)
            start_time = time.time()

            while not self.pc.describe_index(self.index_name).status["ready"]:
                if time.time() - start_time > timeout:
                        raise TimeoutError("Tempo limite excedido para criação do índice no Pinecone.")
                time.sleep(1)
        except Exception as e:
            raise RuntimeError(f"Erro ao criar índice no Pinecone: {e}")
            
       
class PineconeSQLIngestor:
    """
    Classe responsável por ingerir dados SQL no Pinecone.
    """
    def __init__(self,  vector_store: VectorStoreInterface):
        self.vector_store = vector_store

    def get_sql_exemple(self):
        """
        Carrega exemplos SQL de um arquivo CSV e os retorna como um gerador.
        """
        path = 'core/fixtures/sql.csv'

        with open(path, mode='r', encoding='utf-8') as arquivo:
            read = csv.reader(arquivo, delimiter='\t')  # Usando tabulação como separador
            next(read)

            # Ler as linhas do arquivo
            for row in read:
                yield row[0], Document(page_content=row[1], metadata={'sql': row[2]})
    
    def ingest(self):
        """
        Ingestão de dados no Pinecone.
        """
        documents = self.get_sql_exemple()
        for ids, documents in documents:
            print(ids, documents)
            self.vector_store.add_documents(documents=[documents], ids=[ids])
        print('Ingestion finished')
                                    



    
