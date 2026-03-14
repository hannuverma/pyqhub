from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Semester, Subject, Paper


def index(request):
    papers = Paper.objects.all()

    semester = request.GET.get('semester')
    exam_type = request.GET.get('exam')
    subject = request.GET.getlist('subject')
    subjects = Subject.objects.all()

    if semester:
        papers = papers.filter(subject__semester__number=semester)
        subjects = subjects.filter(semester__number=semester)

    if subject:
        papers = papers.filter(subject__id__in=subject)

    if exam_type:
        papers = papers.filter(exam_type=exam_type)

    
    content = {
        'papers': papers,
        "subjects": subjects,
        'semesters': Semester.objects.all(),
        'selected_subjects': subject
    }
    return render(request, 'api/index.html', content)
# Create your views here.
