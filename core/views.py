from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404, StreamingHttpResponse
import time
from sqlalchemy import create_engine
from decouple import config
from langchain_community.utilities import SQLDatabase
from core.forms import MindMapForm
from core.service.mind_map import ChatBot, MindMap
from core.service.memory import ChatHistory, generate_custom_uuid
from core.models import MindMap as Mind
from core.service.graph.graph import graph
from core.service.sql_agent import get_database_backend
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


def text_to_sql(request):
    column_descriptions = (
        ('espacialidades', 'Name of the municipalities', 'Name of the municipalities in the state of Rio de Janeiro'),
        ('nd', 'Development level', 'Classification of the level of human development (Low, Medium, High)'),
        ('mi', 'Infant mortality (%)', 'Infant mortality rate, expressed as a percentage'),
        ('ps60', 'Probability of survival to age 60 (%)', 'Probability of a person surviving to age 60'),
        ('ev', 'Life expectancy at birth', 'Average number of years a person can expect to live at birth'),
        ('ql', 'QL - Locational Quotient', 'Measure that reflects regional inequalities'),
        ('pib', 'GDP (Thousand)', 'Municipal Gross Domestic Product, in thousands of reais'),
        ('rp', 'Per capita income', 'Average income per inhabitant in the municipality'),
        ('gi', 'Gini Index', 'Measure of income inequality, ranging from 0 (total equality) to 1 (maximum inequality)'),
        ('p', '% of poor', 'Percentage of the population considered poor'),
        ('vp', '% vulnerable to poverty', 'Percentage of the population in a situation of vulnerability to poverty'),
        ('fc18', '% of 18 years or older with complete elementary education', 'Percentage of the population aged 18 or older who completed elementary school'),
        ('sc25', '% of 25 years or older with complete higher education', 'Percentage of the population aged 25 or older who completed higher education'),
        ('eae', 'Expected years of schooling', 'Average number of years a child can expect to study during their lifetime'),
        ('t18', 'Illiteracy rate - 18 years or older', 'Percentage of the population aged 18 or older who are illiterate'),
        ('pda', '% of population in households with piped water', 'Percentage of the population living in households with access to piped water'),
        ('pdba', '% of population in households with bathroom and piped water', 'Percentage of the population living in households with a bathroom and piped water'),
        ('pdcl', '% of population in households with regular garbage collection', 'Percentage of the population living in households with regular garbage collection')
    )

    text_description = 'TABLE: idh_data\n\n |Variável|Descrição| \n |---|---|\n'
    # Display the descriptions
    for column, description, description_2  in column_descriptions:
        text_description+=f"|{column}| {description_2}| \n"

    question = request.GET.get("question", "")
    res = graph.invoke({
        'question': question,
        'top_k': 10,
        'dialect': get_database_backend(),
        'table_info': text_description,
    })        
    from pprint import pprint
    pprint(res)
    return JsonResponse(data=res['echart_options']['options'], safe=False)
