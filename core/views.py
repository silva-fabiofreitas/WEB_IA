from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404, StreamingHttpResponse
import time
from sqlalchemy import create_engine
from decouple import config
from core.service.sql_rag import PineconeSQLIngestor, PineconeVectorStoreService
from core.forms import MindMapForm
from core.service.mind_map import ChatBot, MindMap
from core.service.memory import ChatHistory, generate_custom_uuid
from core.models import MindMap as Mind
from core.service.graph.graph import graph
from core.service.sql_agent import FileFormatNotSupported, get_database_backend, ManageTextToSql, TableDescription, LoadDataFrame
from django.views.decorators.csrf import csrf_exempt
import json



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


def dashboard_ia(request):
    return render(request, "core/dashboard_ia.html")


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


@csrf_exempt
def text_to_sql(request):
    question = request.GET.get("question", "")
    manage = ManageTextToSql(LoadDataFrame(),TableDescription())
    table_name = manage.get_table_name(request.user.username, request.user.id)

    if request.method == "POST":
        upload_files = request.FILES['file']
        try:
            df = manage.load_dataframe(upload_files)
        except FileFormatNotSupported:
            return JsonResponse({"error": "Formato de arquivo não suportado"}, status=400)
        
        column_descriptions = manage.get_column_descriptions(df)        
        manage.df_to_sql(df, table_name)

        request.session['table'] = table_name
        request.session['column_descriptions'] = json.dumps(column_descriptions)
        return JsonResponse({"success": 'Carregado com sucesso'}, status=200)

    text_description=manage.table_info(request.session.get('column_descriptions'), table_name)

    res = graph.invoke({
        'question': question,
        'top_k': 10,
        'dialect': get_database_backend(),
        'table_info': text_description,
    })        
    from pprint import pprint
    pprint(res)
    return JsonResponse(data=res['echart_options']['options'], safe=False)


def run_commands(request):
    ingestor = PineconeSQLIngestor(
        PineconeVectorStoreService()
    )
    ingestor.ingest()

    return JsonResponse({"success": "true"}, status=200)
