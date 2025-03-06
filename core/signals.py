from django.db.models.signals import pre_delete
from django.contrib.sessions.models import Session
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import connection, ProgrammingError, transaction, IntegrityError, InternalError

User = get_user_model()

@receiver(pre_delete, sender=Session)
def session_expired(sender, instance, **kwargs):
    # Tenta carregar os dados da sessão para obter o ID do usuário
    session_data = instance.get_decoded()    
    if table_name := session_data.get('table'):
        with connection.cursor() as cursor:
            try:
                with transaction.atomic():
                    cursor.execute(f"DROP TABLE {table_name};")
            except (ProgrammingError, InternalError, IntegrityError) as e:
                print(f"Tabela {table_name} nao existe.")
                return
            print(f"Tabela {table_name} apagada porque a sessão expirou.")
    

        