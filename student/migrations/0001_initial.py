# Generated by Django 5.2 on 2025-05-05 12:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teacher', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected_option', models.IntegerField()),
                ('is_correct', models.BooleanField()),
                ('attempt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='student.examattempt')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.question')),
            ],
        ),
    ]
