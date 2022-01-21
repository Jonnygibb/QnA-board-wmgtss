from django.urls import path
from board import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name = 'home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]