from django.db import models
from django.contrib.auth.models import User


class StudySession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='study_sessions'
    )
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    scheduled_date = models.DateField()
    start_time = models.TimeField()
    duration = models.PositiveIntegerField(default=60)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class StudyTask(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='study_tasks'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
