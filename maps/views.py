from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Node, Edge
from .algorithms import PathfindingAlgorithms


def index(request):
    """Main page with Google Maps integration"""
    nodes = Node.objects.all()
    context = {
        'nodes': nodes,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'maps/index.html', context)


def debug_maps(request):
    """Debug page to test Google Maps loading"""
    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'maps/debug.html', context)


@csrf_exempt
def find_path_api(request):
    """API endpoint for pathfinding"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            start_id = int(data.get('start_id'))
            end_id = int(data.get('end_id'))
            algorithm = data.get('algorithm', 'dijkstra').lower()
            
            # Initialize pathfinding algorithms
            pathfinder = PathfindingAlgorithms()
            result = pathfinder.find_path(start_id, end_id, algorithm)
            
            if result:
                # Get node details for the path
                path_nodes = []
                for node_id in result['path']:
                    node = Node.objects.get(id=node_id)
                    path_nodes.append({
                        'id': node.id,
                        'name': node.name,
                        'latitude': node.latitude,
                        'longitude': node.longitude
                    })
                
                return JsonResponse({
                    'success': True,
                    'path': path_nodes,
                    'path_ids': result['path'],
                    'distance': result['distance'],
                    'nodes_explored': result['nodes_explored'],
                    'execution_time': result['execution_time'],
                    'algorithm': result['algorithm']
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'No path found between the selected nodes'
                })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def get_nodes_api(request):
    """API endpoint to get all nodes"""
    nodes = Node.objects.all()
    nodes_data = []
    
    for node in nodes:
        nodes_data.append({
            'id': node.id,
            'name': node.name,
            'latitude': node.latitude,
            'longitude': node.longitude,
            'description': node.description
        })
    
    return JsonResponse({'nodes': nodes_data})


def get_edges_api(request):
    """API endpoint to get all edges"""
    edges = Edge.objects.select_related('from_node', 'to_node').all()
    edges_data = []
    
    for edge in edges:
        edges_data.append({
            'from_node': {
                'id': edge.from_node.id,
                'name': edge.from_node.name,
                'latitude': edge.from_node.latitude,
                'longitude': edge.from_node.longitude
            },
            'to_node': {
                'id': edge.to_node.id,
                'name': edge.to_node.name,
                'latitude': edge.to_node.latitude,
                'longitude': edge.to_node.longitude
            },
            'weight': edge.weight
        })
    
    return JsonResponse({'edges': edges_data}) 