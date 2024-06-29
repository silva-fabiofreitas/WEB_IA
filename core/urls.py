from django.urls import include, path

from . import views  

urlpatterns = [
    path('', views.home, name='home'),
    path('virtual-assistant', views.virtual_assistant, name='virtual_assistant'),
    path('virtual-assistant/answer/', views.ia_answer, name='virtual_assistant_answer'),
    ]