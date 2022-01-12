from django.urls import path
from board import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]