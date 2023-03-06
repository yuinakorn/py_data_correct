from django.urls import path
from . import views

urlpatterns = [
    path('ncd/', views.search_ncd, name='ncd'),
    path('person/', views.search_person, name='person'),
    path('', views.index, name='index'),
]
