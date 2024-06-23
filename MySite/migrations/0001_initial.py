# Generated by Django 5.0.6 on 2024-06-22 18:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('units', models.PositiveIntegerField()),
                ('level', models.CharField(choices=[('100', '100 Level'), ('200', '200 Level'), ('300', '300 Level'), ('400', '400 Level')], max_length=3)),
                ('semester', models.CharField(choices=[('1', 'First Semester'), ('2', 'Second Semester')], max_length=1)),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MySite.lecturer')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('matric_number', models.CharField(max_length=20, unique=True)),
                ('level', models.CharField(choices=[('100', '100 Level'), ('200', '200 Level'), ('300', '300 Level'), ('400', '400 Level')], max_length=3)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(choices=[('1', 'First Semester'), ('2', 'Second Semester')], max_length=1)),
                ('session', models.CharField(choices=[('2023/2024', '2023/2024'), ('2024/2025', '2024/2025'), ('2025/2026', '2025/2026'), ('2026/2027', '2026/2027'), ('2027/2028', '2027/2028'), ('2028/2029', '2028/2029'), ('2029/2030', '2029/2030')], max_length=9)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MySite.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MySite.student')),
            ],
            options={
                'unique_together': {('student', 'course', 'semester', 'session')},
            },
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('100', '100 Level'), ('200', '200 Level'), ('300', '300 Level'), ('400', '400 Level')], max_length=3)),
                ('day', models.CharField(choices=[('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday')], max_length=3)),
                ('start_time', models.TimeField(choices=[('08:00', '08:00 AM'), ('09:00', '09:00 AM'), ('10:00', '10:00 AM'), ('11:00', '11:00 AM'), ('12:00', '12:00 PM'), ('13:00', '01:00 PM'), ('14:00', '02:00 PM'), ('15:00', '03:00 PM'), ('16:00', '04:00 PM')])),
                ('end_time', models.TimeField(choices=[('08:00', '08:00 AM'), ('09:00', '09:00 AM'), ('10:00', '10:00 AM'), ('11:00', '11:00 AM'), ('12:00', '12:00 PM'), ('13:00', '01:00 PM'), ('14:00', '02:00 PM'), ('15:00', '03:00 PM'), ('16:00', '04:00 PM')])),
                ('semester', models.CharField(choices=[('1', 'First Semester'), ('2', 'Second Semester')], max_length=1)),
                ('session', models.CharField(choices=[('2023/2024', '2023/2024'), ('2024/2025', '2024/2025'), ('2025/2026', '2025/2026'), ('2026/2027', '2026/2027'), ('2027/2028', '2027/2028'), ('2028/2029', '2028/2029'), ('2029/2030', '2029/2030')], max_length=9)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MySite.course')),
            ],
            options={
                'unique_together': {('course', 'day', 'start_time', 'semester', 'session')},
            },
        ),
    ]
