from django.contrib.sessions.models import Session
from django.utils.timezone import now


class ExpiredSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica se a sessão existe
        try:
            Session.objects.filter(expire_date__lt=now()).delete()
        except Session.DoesNotExist:
            pass  # Sessão já foi removida
        return self.get_response(request)


