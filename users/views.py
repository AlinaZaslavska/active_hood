from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView
from users.forms import RegisterForm, LoginForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from users.forms import UpdateUserForm, UpdateProfileForm, ProfileActivityFormSet,  ProfileActivityForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from users.models import ProfileActivity
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST


def home(request):
    return render(request, "users/home.html")


class RegisterView(View):
    form_class = RegisterForm
    initial = {"key": "value"}
    template_name = "users/register.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            try:
                form.save()
                username = form.cleaned_data.get("username")
                messages.success(request, f"Account created for {username}")
                return redirect(to="login")
            except IntegrityError:
                messages.error(request, "An account with that email already exists.")
                return render(request, self.template_name, {"form": form})

        return render(request, self.template_name, {"form": form})

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to="/")

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    profile_instance = request.user.profile
    
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile_instance)
        formset = ProfileActivityFormSet(request.POST, instance=profile_instance, profile=profile_instance)

        if user_form.is_valid() and profile_form.is_valid() and formset.is_valid():
            user_form.save()
            profile_form.save()
            formset.save()
            messages.success(request, 'Your profile is updated successfully!')
            return redirect('users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=profile_instance)
        formset = ProfileActivityFormSet(queryset=ProfileActivity.objects.filter(profile=profile_instance), profile=profile_instance)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'formset': formset,
    }
    return render(request, 'users/profile.html', context)



class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

@login_required
def add_activity(request):
    if request.method == 'POST':
        form = ProfileActivityForm(request.POST, profile=request.user.profile)
        if form.is_valid():
            profile_activity = form.save(commit=False)
            profile_activity.profile = request.user.profile
            profile_activity.save()
            messages.success(request, 'Activity added successfully!')
            return redirect('users-profile')  # Redirect to the profile page or any other
    else:
        form = ProfileActivityForm(profile=request.user.profile)

    context = {'form': form}
    return render(request, 'users/add_activity.html', context)


@login_required
def update_activity(request, activity_id):
    profile_activity = get_object_or_404(ProfileActivity, id=activity_id, profile=request.user.profile)
    
    if request.method == 'POST':
        form = ProfileActivityForm(request.POST, instance=profile_activity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity updated successfully!')
            return redirect('users-profile')  # Redirect after success
    else:
        form = ProfileActivityForm(instance=profile_activity)

    context = {'form': form}
    return render(request, 'users/update_activity.html', context)


@login_required
def delete_activity(request, activity_id):
    profile_activity = get_object_or_404(ProfileActivity, id=activity_id, profile=request.user.profile)
    if request.method == 'POST':
        profile_activity.delete()
        messages.success(request, 'Activity deleted successfully!')
        return redirect('users-profile')  # Redirect after deletion

    context = {'profile_activity': profile_activity}
    return render(request, 'users/delete_activity.html', context)


@require_POST
@login_required
def send_invitation(request):
    email = request.POST.get('email')
    user_email = request.user.email

    if email:
        subject = "You're Invited to Join ActiveHood!"
        message = f"Hi there!\n\n{request.user.first_name} {request.user.last_name} has invited you to join ActiveHood, a vibrant community for sports enthusiasts. Sign up now and connect with like-minded individuals!\n\nBest regards,\nThe ActiveHood Team"
        from_email = settings.DEFAULT_FROM_EMAIL
        try:
            send_mail(subject, message, from_email, [email])
            messages.success(request, f"Invitation sent to {email}!")
        except Exception as e:
            messages.error(request, "Failed to send invitation. Please try again later.")
    
    return redirect('users-home')  # Redirect to the home page or wherever you prefer