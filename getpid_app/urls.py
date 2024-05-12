from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('protected/', views.my_protected_view, name='protected'),
    path('home/', views.home, name='home'),
    path('person/', views.person, name='person'),
    path('hoscode/', views.hoscode, name='hoscode'),
    path('provider/', views.provider, name='provider'),

    path('ncd/', views.ncd, name='ncd'),
    path('labor/', views.labor, name='labor'),
    path('palliative/', views.palliative, name='palliative'),
    path('', views.index, name='index'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


