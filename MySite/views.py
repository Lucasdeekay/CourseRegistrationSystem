import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from MySite.models import Course, Student, CourseRegistration, Timetable
from MySite.serializers import CourseSerializer, CourseRegistrationSerializer


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to successful login page
            return redirect('display_timetable')
        else:
            # Invalid login credentials
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'login.html')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email'].strip()
        try:
            user = User.objects.get(email=email)
            login(request, user)
            return redirect('password_reset')
        except User.DoesNotExist:
            messages.error(request, 'Email address not found.')
            return redirect('forgot_password')
    return render(request, 'forgot_password.html')


def password_reset_view(request):
    user = request.user

    if request.method == 'POST':
        new_password1 = request.POST['new_password1'].strip()
        new_password2 = request.POST['new_password2'].strip()
        if new_password1 != new_password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('password_reset')
        # Set the new password
        user.set_password(new_password1)
        user.save()
        logout(request)
        messages.success(request, 'Password reset successfully!')
        return redirect('login')
    return render(request, 'password_reset.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def get_courses_by_level_and_semester(request):
    if request.method == 'POST' and not request.user.is_superuser:
        student = Student.objects.get(user=request.user)
        level = request.POST.get('level')
        semester = request.POST.get('semester')

        # Get all courses for the level and semester
        all_courses = Course.objects.filter(level=level, semester=semester)

        # Get student's registered courses for the semester
        registered_courses = CourseRegistration.objects.filter(
            student=student, course__level=level, semester=semester
        ).select_related('course')  # Eager loading

        # Exclude registered courses from all courses
        available_courses = all_courses.exclude(id__in=[
            registration.course.id for registration in registered_courses
        ])
        serializer = CourseSerializer(available_courses, many=True)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Unauthorized access or invalid request method.'})


@login_required
def get_registered_courses_by_level_and_semester(request):
    if request.method == 'POST' and not request.user.is_superuser:
        student = Student.objects.get(user=request.user)
        level = request.POST.get('level')
        semester = request.POST.get('semester')

        # Select courses with details from registrations
        registered_courses = CourseRegistration.objects.filter(
            student=student, course__level=level, semester=semester
        ).select_related('course')  # Eager loading to avoid N+1 queries

        # Prepare data with course details and registration ID
        course_data = []
        for registration in registered_courses:
            course = registration.course
            course_data.append({
                'id': registration.id,  # CourseRegistration ID
                'code': course.code,
                'title': course.title,
                'units': course.units,
                # Add other relevant course details as needed
            })

        return JsonResponse(course_data, safe=False)
    else:
        return JsonResponse({'error': 'Unauthorized access or invalid request method.'})


@login_required
def register_courses(request):
    if not request.user.is_superuser:
        student = Student.objects.get(user=request.user)
        if request.method == 'POST':
            selected_courses = request.POST.getlist('course_id')

            for course_id in selected_courses:
                course = Course.objects.get(id=int(course_id))
                # Check if the course registration already exists
                existing_registration = CourseRegistration.objects.filter(student=student, course=course,
                                                                          semester=course.semester,
                                                                          session='2023/2024').exists()

                if not existing_registration:
                    CourseRegistration.objects.create(student=student, course=course, semester=course.semester,
                                                      session='2023/2024')

            messages.success(request, 'Course(s) successfully registered')

            return redirect('register_courses')

        # Handle any error scenario
        return render(request, 'register_courses.html', context={"student": student})
    else:
        messages.error(request, "User access not allowed")
        return redirect('login')


@login_required
def unregister_courses(request):
    if not request.user.is_superuser:
        student = Student.objects.get(user=request.user)
        if request.method == 'POST':
            selected_courses = request.POST.getlist('course_id')

            for reg_id in selected_courses:
                # Delete the course registration if it exists
                CourseRegistration.objects.filter(id=int(reg_id)).delete()

            messages.success(request, 'Course(s) successfully unregistered')

            # You can redirect or return a success response as needed
            return redirect('unregister_courses')

        return render(request, 'registered_courses.html', {'student': student})
    else:
        messages.error(request, "User access not allowed")
        return redirect('login')


@login_required
def display_timetable(request):
    if not request.user.is_superuser:
        student = Student.objects.get(user=request.user)
        level = student.level

        # Retrieve timetable entries for the student's level
        first_timetable_entries = Timetable.objects.filter(level=level, semester='1')
        second_timetable_entries = Timetable.objects.filter(level=level, semester='2')

        for i in first_timetable_entries:
            print(i.start_time)

        context = {
            'first_timetable_entries': first_timetable_entries,
            'second_timetable_entries': second_timetable_entries,
            'student': student,
            'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
            'hours': ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00'],
        }

    else:
        # Retrieve timetable entries for the student's level
        first_timetable_entries_100 = Timetable.objects.filter(level='100', semester='1')
        second_timetable_entries_100 = Timetable.objects.filter(level='100', semester='2')
        first_timetable_entries_200 = Timetable.objects.filter(level='200', semester='1')
        second_timetable_entries_200 = Timetable.objects.filter(level='200', semester='2')
        first_timetable_entries_300 = Timetable.objects.filter(level='300', semester='1')
        second_timetable_entries_300 = Timetable.objects.filter(level='300', semester='2')
        first_timetable_entries_400 = Timetable.objects.filter(level='400', semester='1')
        second_timetable_entries_400 = Timetable.objects.filter(level='400', semester='2')

        context = {
            'first_timetable_entries_100': first_timetable_entries_100,
            'second_timetable_entries_100': second_timetable_entries_100,
            'first_timetable_entries_200': first_timetable_entries_200,
            'second_timetable_entries_200': second_timetable_entries_200,
            'first_timetable_entries_300': first_timetable_entries_300,
            'second_timetable_entries_300': second_timetable_entries_300,
            'first_timetable_entries_400': first_timetable_entries_400,
            'second_timetable_entries_400': second_timetable_entries_400,
            'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
            'hours': ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00'],
            'admin': True,
        }

    return render(request, 'timetable.html', context)


@login_required
def change_password(request):
    student = Student.objects.get(user=request.user)

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # Check if the old password is correct
        if not request.user.check_password(old_password):
            messages.error(request, 'Your old password was entered incorrectly. Please enter it again.')
            return redirect('change_password')

        # Check if the new passwords match
        if new_password1 != new_password2:
            messages.error(request, 'The two new password fields didn\'t match.')
            return redirect('change_password')

        # Update the user's password
        request.user.set_password(new_password1)
        request.user.save()

        # Update the user's session to reflect the password change
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Your password was successfully updated!')
        return redirect('change_password')

    return render(request, 'change_password.html', {'student': student})


def generate_timetable(level, semester, session):
    Timetable.objects.filter(level=level, semester=semester).delete()

    courses = Course.objects.filter(level=level, semester=semester)

    if not courses.exists():
        raise ValueError("No courses available for the specified level and semester")

    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    hours = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00']
    venues = ['CAS 1', 'CAS 2', 'CAS 3', 'HL', 'SL']

    # Initialize timetable slots as a dictionary of lists
    timetable_slots = {day: {hour: [] for hour in hours} for day in days}

    courses = courses.order_by('-units')  # Sort courses by descending units

    # Helper function to get a random slot
    def get_random_slot():
        day = random.choice(days)
        hour = random.choice(hours)
        venue = random.choice(venues)
        return day, hour, venue

    timetable_entries = []

    with transaction.atomic():
        for course in courses:
            assigned_hours = 0
            while assigned_hours < course.units:
                day, hour, venue = get_random_slot()

                start_time = hour
                end_time = f"{int(start_time[:2]) + 1:02}:00"

                # Assign the course to the slot
                timetable_slots[day][hour].append((course, venue))
                timetable_entry = Timetable(
                    course=course,
                    level=level,
                    day=day,
                    start_time=start_time,
                    end_time=end_time,
                    venue=venue,
                    semester=semester,
                    session=session,
                )
                timetable_entries.append(timetable_entry)
                assigned_hours += 1

        # Bulk create timetable entries
        Timetable.objects.bulk_create(timetable_entries)

    return timetable_entries


def generate_timetable_view(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            level = request.POST.get('level')
            semester = request.POST.get('semester')

            # Validate inputs (add more validation as needed)
            if level and semester:
                # Generate timetable using the trusted algorithm
                generate_timetable(level, semester, '2023/2024')

                messages.success(request, f"Timetable successfully generated")

        return render(request, 'generate_timetable.html', {'admin': True})
    else:
        return redirect('display_timetable')


def generate_session_timetable_view(request):
    if request.method == 'POST':
        level = request.POST.get('level')

        # Validate inputs (add more validation as needed)
        if level:
            # Generate timetable using the trusted algorithm
            generate_timetable(level, '1', '2023/2024')
            generate_timetable(level, '2', '2023/2024')

            messages.success(request, f"Timetables successfully generated")

            return redirect('generate_timetable')
