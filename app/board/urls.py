from django.urls import path
from board import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name = 'home'),
    # Cretes a url pattern with a variable to create a url for each post
    path('question/<slug:slug>/', views.QuestionDetailView.as_view(), name = 'question-detail'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]