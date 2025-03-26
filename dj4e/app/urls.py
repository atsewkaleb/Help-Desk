from django.views.generic import TemplateView
from django.urls import path
from .views import create_request, register, request_list, view_request, edit_request, activate
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('requests/', request_list, name='request_list'),
    path('requests/create/', create_request, name='create_request'),
    path('requests/<int:pk>/', view_request, name='view_request'),
    path('requests/<int:pk>/edit/', edit_request, name='edit_request'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('register/', register, name='register'),
]
