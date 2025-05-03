from django.urls import path
from . import views

app_name = 'student'
urlpatterns = [
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/<int:exam_id>/take/', views.take_exam, name='take_exam'),
    path('attempts/<int:attempt_id>/result/', views.exam_result, name='exam_result'),
    path('performance/', views.performance, name='performance'),
]
