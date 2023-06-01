from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.projects, name='projects'),
    path('projects/delete/<int:id>/', views.delete, name='delete'),
    path('projects/details/<slug:slug>/', views.details, name='details'),
    path('projects/start_timer/<int:id>/', views.start_timer, name='start_timer'),
    path('projects/stop_timer/<int:id>/', views.stop_timer, name='stop_timer'),
]
