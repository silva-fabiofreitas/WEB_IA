from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404


# Create your views here.
def home(request):
    return render(request, 'core/base.html')
