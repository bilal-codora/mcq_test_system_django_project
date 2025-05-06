from django.urls import path
from . import views

app_name = 'teacher'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('questions/', views.question_list, name='question_list'),
    path('questions/add/', views.add_question, name='add_question'),
    path('questions/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('questions/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/create/', views.create_exam, name='create_exam'),
    path('exams/<int:exam_id>/results/', views.exam_results, name='exam_results'),
    path('generate_mcq/', views.generate_mcq, name='generate_mcq'),
    # path('upload_dataset/', views.upload_dataset, name='upload_dataset'),
]
