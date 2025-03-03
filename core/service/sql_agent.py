# from django.conf import settings

from django.db import connection


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
