from django.shortcuts import render, redirect, get_object_or_404
import spacy
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Question, Subject, Topic
from .forms import QuestionForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Subject, Topic, Question, Exam
from .forms import SubjectForm, TopicForm, QuestionForm, ExamForm
from student.models import ExamAttempt
from io import BytesIO
import base64
import matplotlib.pyplot as plt
nlp = spacy.load("en_core_web_sm")

# Decorator to allow only teachers
def teacher_required(view_func):
    decorated = user_passes_test(lambda u: u.is_authenticated and u.is_teacher(), login_url='login')(view_func)
    return decorated

@teacher_required
def dashboard(request):
    exams = Exam.objects.filter(teacher=request.user)
    return render(request, 'teacher/dashboard.html', {'exams': exams})

@teacher_required
def question_list(request):
    questions = Question.objects.all()
    return render(request, 'teacher/question_list.html', {'questions': questions})

@teacher_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher:question_list')
    else:
        form = QuestionForm()
    return render(request, 'teacher/question_form.html', {'form': form})

@teacher_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    form = QuestionForm(request.POST or None, instance=question)
    if form.is_valid():
        form.save()
        return redirect('teacher:question_list')
    return render(request, 'teacher/question_form.html', {'form': form})

@teacher_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return redirect('teacher:question_list')

@teacher_required
def exam_list(request):
    exams = Exam.objects.filter(teacher=request.user)
    return render(request, 'teacher/exam_list.html', {'exams': exams})

@teacher_required
def create_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST, teacher=request.user)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.teacher = request.user
            exam.save()
            form.save_m2m()  # Save questions selection
            return redirect('teacher:exam_list')
    else:
        form = ExamForm(teacher=request.user)
    return render(request, 'teacher/exam_form.html', {'form': form})





@teacher_required
def generate_mcq(request):
    exam = get_object_or_404(Exam, teacher=request.user)

    if request.method == 'POST':
        text = request.POST.get('text', '')
        if not text:
            return render(request, 'teacher/generate_mcq.html', {
                'error': 'Please enter text to generate MCQs.',
                'exam': exam
            })

        doc = nlp(text)
        count = 0

        subject = Subject.objects.first() or Subject.objects.create(name="Default Subject")
        topic = Topic.objects.first() or Topic.objects.create(name="Default Topic", subject=subject)

        for sent in doc.sents:
            if count >= 10:
                break

            nouns = [token.text for token in sent if token.pos_ == "NOUN"]
            if nouns:
                answer = nouns[0]
                q_text = sent.text.replace(answer, "_____")
                options = [answer] + nouns[1:4]

                while len(options) < 4:
                    options.append("Option")

                question = Question.objects.create(
                    text=q_text,
                    option1=options[0],
                    option2=options[1],
                    option3=options[2],
                    option4=options[3],
                    correct_option=1,
                    subject=subject,
                    topic=topic,
                    difficulty='Medium'
                )

                exam.questions.add(question)  # 🟢 Link the question to the exam
                count += 1

        messages.success(request, f'Generated {count} questions for the exam.')
        return redirect('teacher:exam_list')

    return render(request, 'teacher/generate_mcq.html', {'exam': exam})








@teacher_required
def exam_results(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id, teacher=request.user)
    attempts = ExamAttempt.objects.filter(exam=exam)
    # Prepare data for chart (score distribution)
    scores = [att.score for att in attempts]
    fig, ax = plt.subplots()
    ax.hist(scores, bins=10, range=(0, 100))
    ax.set_title(f"Score Distribution: {exam.name}")
    ax.set_xlabel('Score')
    ax.set_ylabel('Number of Students')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    image_png = buf.getvalue()
    chart = base64.b64encode(image_png).decode('utf-8')
    return render(request, 'teacher/exam_results.html', {
        'exam': exam,
        'chart': chart,
        'attempts': attempts
    })

