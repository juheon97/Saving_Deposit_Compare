from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [

    path('get_user_info/', views.get_user_info),
    path('update_profile_image/', views.update_profile_image, name='update_profile_image'),
    path('get_user_products/', views.get_user_products),
    path('delete_user_product/<str:type>/<int:product_id>/', views.delete_user_product, name='delete_user_product'),
    path('change_password/', views.change_password, name='change_password'),
    path('find_password/', views.reset_password, name='find_password'),

]