from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('timetracker/', views.timetracker, name='timetracker'),
    path('projects/', views.projects, name='projects'),
    path('projects/details/<slug:slug>/', views.details, name='details'),
]
