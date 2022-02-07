from django.urls import path
from board import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name = 'home'),
    path('questions/new/', views.QuestionCreateView.as_view(), name = 'question-create'),
    path('question/<slug:slug>/update', views.QuestionUpdateView.as_view(), name = 'question-update'),
    path('question/<slug:slug>/delete', views.QuestionDeleteView.as_view(), name = 'question-delete'),
    path('question/<slug:slug>/add_answer', views.AnswerCreateView.as_view(), name = 'answer-create'),
    path('question/<slug:slug>/update_answer/<int:pk>', views.AnswerUpdateView.as_view(), name = 'answer-update'),
    path('question/<slug:slug>/delete_answer/<int:pk>', views.AnswerDeleteView.as_view(), name = 'answer-delete'),
    path('question/<slug:slug>/add_comment', views.CommentCreateView.as_view(), name = 'comment-create'),
    path('question/<slug:slug>/update_comment/<int:pk>', views.CommentUpdateView.as_view(), name = 'comment-update'),
    path('question/<slug:slug>/delete_comment/<int:pk>', views.CommentDeleteView.as_view(), name = 'comment-delete'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]