"""
URL configuration for pathfinder project.
"""
from django.urls import path, include
 
urlpatterns = [
    path('', include('maps.urls')),
] 