from django.contrib.auth import views as vi
from django.urls import include, path

from users.apps import UsersConfig
from users.views import SignUp

app_name = UsersConfig.name

passwords = [
    path(
        'change/',
        vi.PasswordChangeView.as_view(
            template_name='users/password_change_form.html',
        ),
        name='password_change_form',
    ),
    path(
        'change/done/',
        vi.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html',
        ),
        name='password_change_done',
    ),
    path(
        'reset/',
        vi.PasswordResetView.as_view(
            template_name='users/password_reset_form.html',
        ),
        name='password_reset_form',
    ),
    path(
        'reset/done/',
        vi.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        vi.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        vi.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path(
        'logout/',
        vi.LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout',
    ),
    path(
        'login/',
        vi.LoginView.as_view(template_name='users/login.html'),
        name='login',
    ),
    path('password/', include(passwords)),
]
