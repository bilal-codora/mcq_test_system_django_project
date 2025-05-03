# from django.contrib import admin
# from .models import Question, Exam

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('text', 'option1', 'option2', 'option3', 'option4', 'correct_option')
#     search_fields = ('text',)
#     list_filter = ('correct_option',)

# @admin.register(Exam)
# class ExamAdmin(admin.ModelAdmin):
#     list_display = ('title', 'created_at')
#     search_fields = ('title',)
#     ordering = ('-created_at',)
#     filter_horizontal = ('questions',)  # For ManyToMany relationship
