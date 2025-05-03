# from pydoc import text
from django.shortcuts import render, redirect, get_object_or_404
# import nltk
# nltk.data.path.append('/usr/local/share/nltk_data') 
# nltk.download('punkt')
# from nltk.tokenize import sent_tokenize, word_tokenize
import spacy
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Question, Subject, Topic
from .forms import QuestionForm

# Load spaCy model for English
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
    return render(request, 'prof/dashboard.html', {'exams': exams})

@teacher_required
def question_list(request):
    questions = Question.objects.all()
    return render(request, 'prof/question_list.html', {'questions': questions})

@teacher_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prof:question_list')
    else:
        form = QuestionForm()
    return render(request, 'prof/question_form.html', {'form': form})

@teacher_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    form = QuestionForm(request.POST or None, instance=question)
    if form.is_valid():
        form.save()
        return redirect('prof:question_list')
    return render(request, 'prof/question_form.html', {'form': form})

@teacher_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return redirect('prof:question_list')

@teacher_required
def exam_list(request):
    exams = Exam.objects.filter(teacher=request.user)
    return render(request, 'prof/exam_list.html', {'exams': exams})

@teacher_required
def create_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST, teacher=request.user)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.teacher = request.user
            exam.save()
            form.save_m2m()  # Save questions selection
            return redirect('prof:exam_list')
    else:
        form = ExamForm(teacher=request.user)
    return render(request, 'prof/exam_form.html', {'form': form})

@teacher_required
# def generate_mcq(request):
#     if request.method == 'POST':
#         text = request.POST.get('text')
#         if not text:
#             messages.error(request, "Text cannot be empty.")
#             return redirect('prof:generate_mcq')

#         num_q = int(request.POST.get('num_questions', 5))
#         sentences = sent_tokenize(text)
#         count = 0
#         for sent in sentences:
#             if count >= num_q:
#                 break
#             words = word_tokenize(sent)
#             tagged = pos_tag(words)
#             nouns = [word for word, pos in tagged if pos.startswith('NN')]
#             if nouns:
#                 answer = nouns[0]
#                 # Create a simple blank question
#                 q_text = sent.replace(answer, "_____")
#                 # Generate dummy options
#                 options = [answer]
#                 # Add random distractors from nouns
#                 for noun in nouns[1:4]:
#                     options.append(noun)
#                 # Ensure we have four options
#                 while len(options) < 4:
#                     options.append("Option")
#                 form = Question(
#                     text=q_text,
#                     option1=options[0],
#                     option2=options[1],
#                     option3=options[2] if len(options) > 2 else "Option",
#                     option4=options[3] if len(options) > 3 else "Option",
#                     correct_option=1,
#                     subject=Subject.objects.first(),
#                     topic=Topic.objects.first(),
#                     difficulty='Medium'
#                 )
#                 form.save()
#                 count += 1
#         messages.success(request, f'Generated {count} questions from input text.')
#         return redirect('prof:question_list')
#     return render(request, 'prof/generate_mcq.html')



@teacher_required
def generate_mcq(request):
    exam = get_object_or_404(Exam, teacher=request.user)

    if request.method == 'POST':
        text = request.POST.get('text', '')
        if not text:
            return render(request, 'prof/generate_mcq.html', {
                'error': 'Please enter text to generate MCQs.',
                'exam': exam
            })

        doc = nlp(text)
        count = 0

        subject = Subject.objects.first() or Subject.objects.create(name="Default Subject")
        topic = Topic.objects.first() or Topic.objects.create(name="Default Topic", subject=subject)

        for sent in doc.sents:
            if count >= 5:
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
        return redirect('prof:exam_list')

    return render(request, 'prof/generate_mcq.html', {'exam': exam})







@teacher_required
def upload_dataset(request):
    if request.method == 'POST':
        file = request.FILES['file']
        import pandas as pd
        df = pd.read_csv(file)
        for _, row in df.iterrows():
            Question.objects.create(
                text=row['text'],
                option1=row['option1'],
                option2=row['option2'],
                option3=row['option3'],
                option4=row['option4'],
                correct_option=int(row['correct_option']),
                explanation=row.get('explanation', ''),
                subject=Subject.objects.get_or_create(name=row['subject'])[0],
                topic=Topic.objects.get_or_create(name=row['topic'], subject=Subject.objects.get_or_create(name=row['subject'])[0])[0],
                difficulty=row['difficulty']
            )
        messages.success(request, "Dataset imported successfully.")
        return redirect('prof:question_list')
    return render(request, 'prof/upload_dataset.html')

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
    return render(request, 'prof/exam_results.html', {
        'exam': exam,
        'chart': chart,
        'attempts': attempts
    })
