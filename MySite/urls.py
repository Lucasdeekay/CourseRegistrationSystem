from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .viewsets import StudentViewSet, CourseViewSet, TimetableViewSet, CourseRegistrationViewSet, LecturerViewSet

router = DefaultRouter()
router.register(r'lecturers', LecturerViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'students', StudentViewSet)
router.register(r'timetables', TimetableViewSet)
router.register(r'course-registrations', CourseRegistrationViewSet)


urlpatterns = [
    # AJAX views
    path('get_courses/', views.get_courses_by_level_and_semester, name='get_courses'),
    path('get_registered_courses/', views.get_registered_courses_by_level_and_semester,
         name='get_registered_courses'),

    # HTML views
    path('', views.login_view, name='login'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/', views.password_reset_view, name='password_reset'),
    path('logout/', views.logout_view, name='logout'),
    path('register_courses/', views.register_courses, name='register_courses'),
    path('unregister_courses/', views.unregister_courses, name='unregister_courses'),
    path('timetable/', views.display_timetable, name='display_timetable'),
    path('change_password/', views.change_password, name='change_password'),
    path('generate_timetable/', views.generate_timetable_view, name='generate_timetable'),
    path('generate_session_timetable/', views.generate_session_timetable_view, name='generate_session_timetable'),

    # API views
    path('api/', include(router.urls)),
]
