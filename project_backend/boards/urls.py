from django.urls import path
from . import views

app_name='boards'
urlpatterns = [ 
    path('board1/', views.board_list, {'board_type': 'board1'}),
    path('board2/', views.board_list, {'board_type': 'board2'}),
    path('board3/', views.board_list, {'board_type': 'board3'}),
    # path('', views.board_list),  # 이미 /boards/로 접근됨
    path('<str:board_type>/<int:board_pk>/', views.board_detail),
    # path('<int:board_pk>/', views.board_detail), # 이미 /boards/1/로 접근됨
    path('<str:board_type>/<int:board_pk>/like/', views.board_like),
    # path('<int:board_pk>/like/', views.board_like),
    path('<str:board_type>/<int:board_pk>/comments/', views.comment_list),
    path('<str:board_type>/<int:board_pk>/comments/<int:comment_pk>/', views.comment_detail),
    path('<str:board_type>/<int:board_pk>/comments/<int:comment_pk>/like/', views.comment_like),
    # path('<int:board_pk>/comments/', views.comment_list),
    # path('<int:board_pk>/comments/<int:comment_pk>/', views.comment_detail),
    # path('<int:board_pk>/comments/<int:comment_pk>/like/', views.comment_like),
]
