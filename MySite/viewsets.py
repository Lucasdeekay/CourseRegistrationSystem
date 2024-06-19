from rest_framework import viewsets
from .models import Lecturer, Course, Student, Timetable, CourseRegistration
from .serializers import LecturerSerializer, CourseSerializer, StudentSerializer, TimetableSerializer, \
    CourseRegistrationSerializer


class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer


class CourseRegistrationViewSet(viewsets.ModelViewSet):
    queryset = CourseRegistration.objects.all()
    serializer_class = CourseRegistrationSerializer
