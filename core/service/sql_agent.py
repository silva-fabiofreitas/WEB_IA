import json
from abc import ABC, abstractmethod

import pandas as pd
from decouple import config
from django.db import connection
from sqlalchemy import create_engine

from langchain_community.utilities import SQLDatabase


def get_database_backend():
    engine = connection.settings_dict['ENGINE']
    if 'sqlite' in engine:
        return "SQLite"
    elif 'postgresql' in engine:
        return "PostgreSQL"
    elif 'mysql' in engine:
        return "MySQL"
    elif 'oracle' in engine:
        return "Oracle"
    return "Outro banco de dados"


def get_engine():
    POSTGRES_NAME = config('POSTGRES_NAME')
    POSTGRES_USER = config('POSTGRES_USER')
    POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
    POSTGRES_HOST = config('POSTGRES_HOST')
    POSTGRES_PORT = config('POSTGRES_PORT')
        
    DATABASE_URL = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"

    # Criando a engine do SQLAlchemy
    return create_engine(DATABASE_URL)


class FileFormatNotSupported(Exception):
    """File format not supported"""
    pass


class DataLoaderStrategy(ABC):
    @abstractmethod
    def load(self, upload_files) -> pd.DataFrame:
        pass


class LoadCsv(DataLoaderStrategy):
    def load(self, upload_files) -> pd.DataFrame:
        return pd.read_csv(upload_files)


class LoadExcel(DataLoaderStrategy):
    def load(self, upload_files) -> pd.DataFrame:
        return pd.read_excel(upload_files)
    

class LoadDataFrame: 
    def __init__(self, strategies: dict[str, DataLoaderStrategy] = None):
        self.strategies = strategies or self._strategy_load_default()


    def _get_file_format(self, upload_files) -> str:
        """
        Extract the file format from the uploaded file.
        """
        return upload_files.name.split('.')[-1]
    
    @staticmethod
    def _strategy_load_default() -> dict[str, DataLoaderStrategy]:
        """
        Define the strategy for loading dataframes based on file format.
        """
        return dict(
            csv=LoadCsv(),
            xlsx=LoadExcel(),
            xls=LoadExcel()
        )
        
    def load_dataframe(self, upload_files) -> pd.DataFrame:
        """
        Load a dataframe from the uploaded file.
        """
        file_format = self._get_file_format(upload_files)
        if file_format not in self.strategies:
            raise FileFormatNotSupported(f"Formato de arquivo '{file_format}' não suportado")
        return self.strategies[file_format].load(upload_files)
    
    def df_to_sql(self, df: pd.DataFrame, table_name: str) -> None:
        """
        Save the dataframe to a SQL table.
        """
        engine = get_engine()
        df.columns = df.columns.str.lower()
        try:
            df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        finally:
            engine.dispose()


class TableDescription:
    def get_table_name(self, user: str, _id: str) -> str:
        """
        Generate a table name based on user and id.
        """
        return f"data_{user.lower()}_{_id or 'table'}"
    
    def table_description(self, column_descriptions: str, table_name: str) -> str:
        """
        Generate a table description.
        """
        if column_descriptions:
            return self._table_description_from_session(column_descriptions, table_name)
        return self._table_description_from_db(table_name)

    def get_column_descriptions(self, df: pd.DataFrame) -> dict:
        """
        Get descriptions of the columns in the dataframe.
        """
        if df.iloc[-1, :].apply(lambda x: isinstance(x, str)).all():
            df.drop(df.tail(1).index, inplace=True)
            return df.iloc[-1, :].to_dict()
        return df.iloc[1, :].apply(lambda x: str(type(x))).to_dict()
    
    def _table_description_from_session(self, column_descriptions: str, table_name: str) -> str:
        """
        Generate a table description from session data.
        """
        column_descriptions = json.loads(column_descriptions)
        text_description = f'TABLE: {table_name}\n\n OBS.: \n |Variável|Descrição| \n |---|---|\n'
        for column, description in column_descriptions.items():
            text_description += f"|{column}| {description}| \n"
        return text_description
    
    def _table_description_from_db(self, table_name: str) -> str:
        """
        Generate a table description from the database.
        """
        with get_engine().connect() as connection:
            db = SQLDatabase(engine=connection.engine)
            table_info = db.get_table_info([table_name])
        return table_info


class ManageTextToSql:
    def __init__(self, manage_dataframe:LoadDataFrame, table_description: TableDescription):
        self.manage_dataframe = manage_dataframe
        self.table_description = table_description
    
    def get_table_name(self, user: str, _id: str) -> str:
        """
        Generate a table name based on user and id.
        """
        return self.table_description.get_table_name(user, _id)
    
    def load_dataframe(self, upload_files) -> pd.DataFrame:
        """
        Load a dataframe from the uploaded file.
        """
        return self.manage_dataframe.load_dataframe(upload_files)
    
    def df_to_sql(self, df: pd.DataFrame, table_name: str) -> None:
        """
        Save the dataframe to a SQL table.
        """
        self.manage_dataframe.df_to_sql(df, table_name)

    def table_info(self, column_descriptions: str, table_name: str) -> str:
        """
        Generate a table description.
        """
        return self.table_description.table_description(column_descriptions, table_name)
    
    def get_column_descriptions(self, df: pd.DataFrame) -> dict:
        """
        Get descriptions of the columns in the dataframe.
        """
        return self.table_description.get_column_descriptions(df)
        