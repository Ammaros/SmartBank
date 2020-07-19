from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome-page'),
    path('login/', views.login_view, name='login-page'),
    path('signup/', views.signup_view, name='signup-page'),
    path('logout', views.logout_view, name="logout"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transfer/', views.transfer, name='transfer'),
    path('transactions/', views.transactions, name='transactions'),
]
