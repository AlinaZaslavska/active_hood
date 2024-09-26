from users.views import home, RegisterView, CustomLoginView, profile
from django.contrib.auth import views as auth_views
from users.forms import LoginForm
from django.urls import path, include, re_path
from users.views import ResetPasswordView
from django.conf import settings
from django.conf.urls.static import static
from users.views import ChangePasswordView, add_activity, update_activity,  delete_activity, send_invitation


urlpatterns = [
    path("", home, name="users-home"),
        path('add-activity/', add_activity, name='add-activity'),
    path('update-activity/<int:activity_id>/', update_activity, name='update-activity'),
    path('delete-activity/<int:activity_id>/', delete_activity, name='delete-activity'),
    path("register/", RegisterView.as_view(), name="users-register"),
    path(
        "login/",
        CustomLoginView.as_view(
            redirect_authenticated_user=True,
            template_name="users/login.html",
            authentication_form=LoginForm,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    # Include the social auth's URLs
    re_path(r"^oauth/", include("social_django.urls", namespace="social")),

    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('profile/', profile, name='users-profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('send-invitation/', send_invitation, name='send_invitation'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

