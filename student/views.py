from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from prof.models import Exam, Question
from .models import ExamAttempt, StudentAnswer
import matplotlib.pyplot as plt
from io import BytesIO
import base64

@login_required
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'student/exam_list.html', {'exams': exams})

@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    questions = exam.questions.all()
    for q in questions:
        q.options = [q.option1, q.option2, q.option3, q.option4]
    if request.method == 'POST':
        # Save student answers and calculate score
        correct_count = 0
        total = questions.count()
        for q in questions:
            selected = int(request.POST.get(f'question_{q.id}', 0))
            is_correct = (selected == q.correct_option)
            if is_correct:
                correct_count += 1
            StudentAnswer.objects.create(
                attempt=None,  # set later after creating attempt
                question=q,
                selected_option=selected,
                is_correct=is_correct
            )
        score = int((correct_count / total) * 100) if total > 0 else 0
        attempt = ExamAttempt.objects.create(student=request.user, exam=exam, score=score)
        # Associate answers with the attempt
        for ans in StudentAnswer.objects.filter(attempt=None):
            ans.attempt = attempt
            ans.save()
        return redirect('student:exam_result', attempt_id=attempt.id)
    return render(request, 'student/take_exam.html', {'exam': exam, 'questions': questions})

@login_required
def exam_result(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, pk=attempt_id, student=request.user)
    answers = attempt.answers.all()
    return render(request, 'student/exam_result.html', {'attempt': attempt, 'answers': answers})

@login_required
def performance(request):
    attempts = ExamAttempt.objects.filter(student=request.user).order_by('timestamp')
    scores = [att.score for att in attempts]
    dates = [att.timestamp.strftime("%d-%m") for att in attempts]
    # Plot performance chart
    if attempts:
        plt.figure(figsize=(6,4))
        plt.plot(dates, scores, marker='o')
        plt.ylim(0, 100)
        plt.title("Your Performance Over Time")
        plt.xlabel("Date")
        plt.ylabel("Score")
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        chart = base64.b64encode(buf.getvalue()).decode()
    else:
        chart = None
    return render(request, 'student/performance.html', {'chart': chart, 'attempts': attempts})
