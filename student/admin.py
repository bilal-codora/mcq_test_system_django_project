from django.contrib import admin
from .models import ExamAttempt, StudentAnswer


class StudentAnswerInline(admin.TabularInline):
    model = StudentAnswer
    extra = 0
    readonly_fields = ('question', 'selected_option', 'is_correct')


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'exam', 'score', 'timestamp')
    list_filter = ('exam', 'student')
    search_fields = ('student__username', 'exam__name')
    inlines = [StudentAnswerInline]


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'attempt', 'question', 'selected_option', 'is_correct')
    list_filter = ('is_correct', 'selected_option')
    search_fields = ('question__text', 'attempt__student__username')
