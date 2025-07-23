from django.urls import path
from . import views

# Set the app namespace for URL reversing
app_name = 'maps'

# URL patterns for the maps app
urlpatterns = [
    path('', views.index, name='index'),  # Main page with map and controls
    path('api/find-path/', views.find_path_api, name='find_path_api'),  # API: Find path between nodes
    path('api/nodes/', views.get_nodes_api, name='get_nodes_api'),      # API: Get all nodes
    path('api/edges/', views.get_edges_api, name='get_edges_api'),      # API: Get all edges
] 