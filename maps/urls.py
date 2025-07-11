from django.urls import path
from . import views

app_name = 'maps'

urlpatterns = [
    path('', views.index, name='index'),
    path('debug/', views.debug_maps, name='debug_maps'),
    path('api/find-path/', views.find_path_api, name='find_path_api'),
    path('api/nodes/', views.get_nodes_api, name='get_nodes_api'),
    path('api/edges/', views.get_edges_api, name='get_edges_api'),
] 