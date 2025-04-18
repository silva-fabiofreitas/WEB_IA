from django.urls import include, path

from . import views  

urlpatterns = [
    path('', views.home, name='home'),
    path('virtual-assistant', views.virtual_assistant, name='virtual_assistant'),
    path('virtual-assistant/answer/', views.ia_answer, name='virtual_assistant_answer'),
    path('mind-map/create/', views.mind_map_save, name='mind_map_create'),
    path('mind-map/list/', views.mind_map_list, name='mind_map_list'),
    path('stream/', views.streaming_view, name='stream'),
    path('chatbot/', views.chat_bot, name='chat_bot'),
    path('dashboard-ia/', views.dashboard_ia, name='dashboard_ia'),
    path('text-to-sql/', views.text_to_sql, name='text_to_sql'),
    path('run-commands/', views.run_commands, name='run_commands'),
    ]