from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/create/', views.create_user_view, name='create_user'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('toggle-user-status/', views.toggle_user_status, name='toggle_user_status'),
]

