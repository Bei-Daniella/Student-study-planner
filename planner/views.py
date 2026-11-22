from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import StudySession, StudyTask


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):

    sessions = StudySession.objects.filter(
        user=request.user
    ).order_by('scheduled_date', 'start_time')

    tasks = StudyTask.objects.filter(
        user=request.user
    ).order_by('-created_at')

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_completed=True).count()
    pending_tasks = tasks.filter(is_completed=False).count()

    if total_tasks > 0:
        progress = round((completed_tasks / total_tasks) * 100)
    else:
        progress = 0

    upcoming_sessions = sessions.filter(
        scheduled_date__gte=timezone.localdate()
    )[:5]

    recent_tasks = tasks[:5]

    context = {
        'sessions': sessions,
        'upcoming_sessions': upcoming_sessions,
        'recent_tasks': recent_tasks,
        'total_sessions': sessions.count(),
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'progress': progress,
    }

    return render(request, 'dashboard.html', context)
