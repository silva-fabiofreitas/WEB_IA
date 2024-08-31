from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404, StreamingHttpResponse
import time
from core.forms import MindMapForm
from core.service.mind_map import ChatBot, MindMap
from core.service.memory import ChatHistory, generate_custom_uuid
from core.models import MindMap as Mind
import uuid
import asyncio



# Create your views here.
def home(request):
    return render(request, "core/home.html")


def virtual_assistant(request):
    form = MindMapForm()
    return render(request, "core/virtual_assistant.html", {"form": form})


def ia_answer(request):
    question = request.GET.get("question", "")
    if question:
        answer = MindMap(question).invoke()

    return JsonResponse({"answer": answer})


def mind_map_save(request):
    form = MindMapForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"create": "true"}, status=200)

    return JsonResponse({"success": False, "errors": form.errors}, status=402)


def mind_map_list(request):
    map = Mind.objects.all()
    return render(request, "core/mind_map_list.html", {"maps": map})


def chat_bot(request):
    question = request.GET.get("question", "")
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"    
    session_id = generate_custom_uuid(f'{request.user.username}:{request.user.id}')
    if is_ajax:
        res = ChatHistory().stream(question,session_id)        
        return StreamingHttpResponse(res)

    return render(request, "core/chat_bot.html")


def stream_data():
    # Generate data in chunks
    for i in range(10):
        yield f"Data chunk {i}\n"
        # Simulate delay between chunks
        time.sleep(1)
        # asyncio.sleep(1)


async def streaming_view(request):
    response = StreamingHttpResponse(stream_data())
    response["Content-Type"] = "text/plain"
    return response
