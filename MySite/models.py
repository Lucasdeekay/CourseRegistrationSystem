from django.db import models
from django.contrib.auth.models import User

# Choices
LEVEL_CHOICES = [
    ('100', '100 Level'),
    ('200', '200 Level'),
    ('300', '300 Level'),
    ('400', '400 Level'),
]

SEMESTER_CHOICES = [
    ('1', 'First Semester'),
    ('2', 'Second Semester'),
]

SESSION_CHOICES = [
    ('2023/2024', '2023/2024'),
    ('2024/2025', '2024/2025'),
    ('2025/2026', '2025/2026'),
    ('2026/2027', '2026/2027'),
    ('2027/2028', '2027/2028'),
    ('2028/2029', '2028/2029'),
    ('2029/2030', '2029/2030'),
]

DAY_CHOICES = [
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'),
    ('Fri', 'Friday'),
]

HOUR_CHOICES = [
    ('08:00', '08:00 AM'),
    ('09:00', '09:00 AM'),
    ('10:00', '10:00 AM'),
    ('11:00', '11:00 AM'),
    ('12:00', '12:00 PM'),
    ('13:00', '01:00 PM'),
    ('14:00', '02:00 PM'),
    ('15:00', '03:00 PM'),
    ('16:00', '04:00 PM'),
]


# Models
class Lecturer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=100)
    units = models.PositiveIntegerField()
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES)
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code} - {self.title}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    matric_number = models.CharField(max_length=20, unique=True)
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES)

    def __str__(self):
        return self.matric_number


class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES)
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField(choices=HOUR_CHOICES)
    end_time = models.TimeField(choices=HOUR_CHOICES)
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
    session = models.CharField(max_length=9, choices=SESSION_CHOICES)

    class Meta:
        unique_together = ('course', 'day', 'start_time', 'semester', 'session')

    def __str__(self):
        return f"{self.course.code} - {self.level} Level - {self.day} {self.start_time}-{self.end_time}"


class CourseRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
    session = models.CharField(max_length=9, choices=SESSION_CHOICES)

    class Meta:
        unique_together = ('student', 'course', 'semester', 'session')

    def __str__(self):
        return f"{self.student.matric_number} - {self.course.code} ({self.semester}, {self.session})"
