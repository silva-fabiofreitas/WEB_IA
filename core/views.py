from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404

from core.forms import MindMapForm
from core.service.mind_map import MindMap
from core.models import MindMap as Mind


# Create your views here.
def home(request):
    return render(request, 'core/home.html')


def virtual_assistant(request):
    form = MindMapForm()
    return render(request, 'core/virtual_assistant.html', {'form':form})



def ia_answer(request):
    question = request.GET.get('question', '')
    answer = question and MindMap(question).invoke() 
    return JsonResponse({'answer':answer})


def mind_map_save(request):
    form = MindMapForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'create':'true'}, status=200)

    return JsonResponse({'success': False, 'errors': form.errors}, status=402)


def mind_map_list(request):
    map = Mind.objects.all()
    return render(request, 'core/mind_map_list.html', {'maps':map})