from django.urls import path
from board import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name = 'home'),
    # Cretes a url pattern with a variable to create a url for each post
    path('question/<slug:slug>/', views.QuestionDetailView.as_view(), name = 'question-detail'),
    path('question/<slug:slug>/update', views.QuestionUpdateView.as_view(), name = 'question-update'),
    path('question/<slug:slug>/delete', views.QuestionDeleteView.as_view(), name = 'question-delete'),
    path('question/<slug:slug>/add_answer', views.AnswerCreateView.as_view(), name = 'answer-create'),
    path('question/<slug:slug>/add_comment', views.CommentCreateView.as_view(), name = 'comment-create'),
    path('question/<slug:slug>/delete_comment/<int:pk>', views.CommentDeleteView.as_view(), name = 'comment-delete'),
    path('questions/new/', views.QuestionCreateView.as_view(), name = 'question-create'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]