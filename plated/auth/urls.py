from django.urls import path
from django.contrib.auth import views

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name="login"),

    path('logout/', views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),

    path('password-reset-confirm/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name="password_reset_confirm"),

    path('password-reset/done/',
        views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name="password_reset_done"),

    path('password-reset-complete/',
        views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name="password_reset_complete"),
]
