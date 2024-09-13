from django.urls import path
from . import views



urlpatterns = [

    path('', views.settings, name='profile'),

    path('change_password/', views.change_passowrd, name='change_password'),

    path('delete_account/', views.delete_account, name='delete_account'),

    path('register/', views.register, name="register"),

    path('password-reset/', views.reset_password, name="password_reset"),
]
