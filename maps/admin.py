from django.contrib import admin
from .models import Node, Edge


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude', 'description']
    list_filter = ['name']
    search_fields = ['name', 'description']


@admin.register(Edge)
class EdgeAdmin(admin.ModelAdmin):
    list_display = ['from_node', 'to_node', 'weight']
    list_filter = ['weight']
    search_fields = ['from_node__name', 'to_node__name'] 