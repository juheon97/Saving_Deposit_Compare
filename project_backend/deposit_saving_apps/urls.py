from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [

    path('save_deposit_products/', views.save_deposit_products),
    path('save_saving_products/', views.save_saving_products),
    path('get_deposit_products/', views.get_deposit_products),
    path('get_deposit_options/', views.get_deposit_options),
    path('get_saving_products/', views.get_saving_products),
    path('get_saving_options/', views.get_saving_options),
    path('toggle_contain/', views.toggle_container),
    path('contained_products/', views.get_contained_products),

]
