from django.urls import path
from . import views
# from .views import handler404

urlpatterns = [
    path('person/', views.person, name='person'),
    path('ncd/', views.ncd, name='ncd'),
    path('labor/', views.labor, name='labor'),
    path('palliative/', views.palliative, name='palliative'),
    path('', views.index, name='index'),
]


