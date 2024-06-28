from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404


# Create your views here.
def home(request):
    return render(request, 'core/home.html')


def virtual_assistant(request):
    return render(request, 'core/virtual_assistant.html')

def ia_answer(request):
    return JsonResponse()
