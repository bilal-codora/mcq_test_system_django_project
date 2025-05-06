from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def is_teacher(self):
        return self.role == 'teacher'

    def is_student(self):
        return self.role == 'student'
    
    def save(self, *args, **kwargs):
        if self.role == 'teacher':
            self.is_superuser = True
            self.is_active = True
            self.is_staff = True
        super().save(*args, **kwargs)
