from itertools import permutations

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from MySite.models import Course, Student, CourseRegistration, Timetable, Lecturer
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
            return redirect('user_dashboard')  # Replace 'home' with your desired redirect URL
        else:
            # Invalid login credentials
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'change_password.html')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email'].strip()
        try:
            user = User.objects.get(email=email)
            return redirect('password_reset', args=(user.id,))
        except User.DoesNotExist:
            messages.error(request, 'Email address not found.')
            return redirect('forgot_password')
    return render(request, 'forgot_password.html')


def password_reset_view(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Invalid user ID.')
        return redirect('password_reset')

    if request.method == 'POST':
        new_password1 = request.POST['new_password1'].strip()
        new_password2 = request.POST['new_password2'].strip()
        if new_password1 != new_password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('password_reset')
        # Set the new password
        user.set_password(new_password1)
        user.save()
        messages.success(request, 'Password reset successfully!')
        return redirect('password_reset')
    return render(request, 'password_reset.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def get_courses_by_level_and_semester(request):
    if request.method == 'POST' and not request.user.is_superuser:
        level = request.POST.get('level')
        semester = request.POST.get('semester')

        courses = Course.objects.filter(level=level, semester=semester)
        serializer = CourseSerializer(courses, many=True)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Unauthorized access or invalid request method.'})


@login_required
def get_registered_courses_by_level_and_semester(request):
    if request.method == 'POST' and not request.user.is_superuser:
        student = Student.objects.get(user=request.user)
        level = request.POST.get('level')
        semester = request.POST.get('semester')

        registrations = CourseRegistration.objects.filter(student=student, course__level=level,
                                                          semester=semester)
        serializer = CourseRegistrationSerializer(registrations, many=True)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Unauthorized access or invalid request method.'})


@login_required
@require_POST
def register_courses(request):
    if not request.user.is_superuser:
        student = Student.objects.get(user=request.user)
        if request.method == 'POST':
            selected_courses = request.POST.getlist('course_id')

            for course_id in selected_courses:
                course = Course.objects.get(id=course_id)
                # Check if the course registration already exists
                existing_registration = CourseRegistration.objects.filter(student=student, course=course,
                                                                          semester=course.semester,
                                                                          session='2023/2024').exists()

                if not existing_registration:
                    CourseRegistration.objects.create(student=student, course=course, semester=course.semester,
                                                      session='2023/2024')

            return redirect('register_courses')

        # Handle any error scenario
        return render(request, 'register_courses.html', context={"student": student})
    else:
        messages.error(request, "User access not allowed")
        return redirect('login')


@login_required
@require_POST
def unregister_courses(request):
    if not request.user.is_superuser:
        student = Student.objects.get(user=request.user)
        if request.method == 'POST':
            selected_courses = request.POST.getlist('courses')
            semester = request.POST.get('semester')

            for course_id in selected_courses:
                course = Course.objects.get(id=course_id)
                # Delete the course registration if it exists
                CourseRegistration.objects.filter(student=student, course=course, semester=semester,
                                                  session='2023/2024').delete()

            # You can redirect or return a success response as needed
            return redirect('registered_courses')

        return render(request, 'register_courses.html')
    else:
        messages.error(request, "User access not allowed")
        return redirect('login')


@login_required
def display_timetable(request):
    if not request.user.is_superuser:
        student = Student.objects.get(user=request.user)
        level = student.level

    # Retrieve timetable entries for the student's level
    timetable_entries = Timetable.objects.filter(level=level)

    context = {
        'timetable_entries': timetable_entries,
        'student_level': level,
    }

    return render(request, 'timetable.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        user = request.user

        # Check if the old password is correct
        if not user.check_password(old_password):
            messages.error(request, 'Your old password was entered incorrectly. Please enter it again.')
            return redirect('change_password')

        # Check if the new passwords match
        if new_password1 != new_password2:
            messages.error(request, 'The two new password fields didn\'t match.')
            return redirect('change_password')

        # Update the user's password
        user.set_password(new_password1)
        user.save()

        # Update the user's session to reflect the password change
        update_session_auth_hash(request, user)

        messages.success(request, 'Your password was successfully updated!')
        return redirect('change_password')

    return render(request, 'change_password.html')


def generate_timetable(level, semester, session):
    courses = Course.objects.filter(level=level, semester=semester)

    if not courses.exists():
        raise ValueError("No courses available for the specified level and semester")

    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    hours = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00']

    # Initialize timetable slots as a dictionary
    timetable_slots = {day: {hour: None for hour in hours} for day in days}

    courses = courses.order_by('-units')  # Sort courses by descending units

    # Helper function to get the next available slot
    def get_next_available_slot():
        for day in days:
            for hour in hours:
                if timetable_slots[day][hour] is None:
                    return day, hour
        return None, None

    timetable_entries = []

    with transaction.atomic():
        for course in courses:
            assigned_hours = 0
            while assigned_hours < course.units:
                day, hour = get_next_available_slot()
                if day is None or hour is None:
                    raise ValueError("Not enough slots to accommodate all courses")

                start_time = hour
                # Calculate the end_time by adding one hour to start_time
                end_time = f"{int(start_time[:2]) + 1:02}:00"

                # Assign the course to the slot
                timetable_slots[day][hour] = course
                timetable_entry = Timetable(
                    course=course,
                    level=level,
                    day=day,
                    start_time=start_time,
                    end_time=end_time,
                    semester=semester,
                    session=session,
                )
                timetable_entries.append(timetable_entry)
                assigned_hours += 1

        # Bulk create timetable entries
        Timetable.objects.bulk_create(timetable_entries)

    return timetable_entries


@user_passes_test(lambda u: u.is_superuser)
def generate_timetable_view(request):
    if request.method == 'POST':
        level = request.POST.get('level')
        semester = request.POST.get('semester')

        # Validate inputs (add more validation as needed)
        if level and semester:
            # Generate timetable using the trusted algorithm
            timetable_entries = generate_timetable(level, semester, '2023/2024')

            context = {
                'timetable_entries': timetable_entries,
                'level': level,
                'semester': semester,
            }
            return render(request, 'generated_timetable.html', context)

    return render(request, 'generate_timetable.html')
