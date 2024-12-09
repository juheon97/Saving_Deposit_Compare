from django.urls import path
from . import views

app_name = 'exchanges'
urlpatterns = [
    path('get_exchange/', views.get_exchange),
    path('get_exchange_info/', views.get_exchange_info),
]