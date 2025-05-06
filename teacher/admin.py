from django.contrib import admin
from .models import Subject, Topic, Question, Exam


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject')
    list_filter = ('subject',)
    search_fields = ('name',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_text', 'subject', 'topic', 'difficulty', 'correct_option')
    list_filter = ('subject', 'topic', 'difficulty')
    search_fields = ('text',)

    def short_text(self, obj):
        return obj.text[:75] + '...' if len(obj.text) > 75 else obj.text
    short_text.short_description = 'Question'


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject', 'teacher', 'time_limit', 'created_at')
    list_filter = ('subject', 'teacher')
    search_fields = ('name', 'description')
    filter_horizontal = ('questions',)
