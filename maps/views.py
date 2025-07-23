# Import necessary Django and project modules
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import json
from .models import Node, Edge
from .algorithms import PathfindingAlgorithms


def index(request):
    """Main page with Google Maps integration"""
    # Fetch all nodes from the database
    nodes = Node.objects.all()
    # Prepare context for rendering the template
    context = {
        'nodes': nodes,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'csrf_token': get_token(request),
    }
    # Render the main index page
    return render(request, 'maps/index.html', context)


@csrf_exempt
# API endpoint to find a path between two nodes using a selected algorithm
# Accepts POST requests with start_id, end_id, and algorithm
# Returns path details and performance metrics as JSON

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
                
                # Return path and metrics as JSON
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
                # No path found
                return JsonResponse({
                    'success': False,
                    'error': 'No path found between the selected nodes'
                })
        
        except Exception as e:
            # Handle errors and return as JSON
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    # Only POST requests are allowed
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# API endpoint to get all nodes in the graph
# Returns a list of nodes with their details as JSON

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


# API endpoint to get all edges in the graph
# Returns a list of edges with node details and weights as JSON

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