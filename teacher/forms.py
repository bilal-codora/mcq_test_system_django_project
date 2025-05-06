from django import forms
from .models import Subject, Topic, Question, Exam

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['subject', 'name']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text','option1','option2','option3','option4','correct_option','explanation','subject','topic','difficulty']

class ExamForm(forms.ModelForm):
    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Exam
        fields = ['name','description','subject','time_limit','questions']
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            # Filter questions to those created by this teacher's subjects
            self.fields['questions'].queryset = Question.objects.filter(subject__in=Subject.objects.all())
