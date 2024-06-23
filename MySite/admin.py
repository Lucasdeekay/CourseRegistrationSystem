from django.contrib import admin
from .models import Lecturer, Course, Student, Timetable, CourseRegistration


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'units', 'level', 'semester', 'lecturer']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'matric_number', 'level']


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['course', 'level', 'day', 'start_time', 'end_time', 'semester', 'session']


@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'semester', 'session']
