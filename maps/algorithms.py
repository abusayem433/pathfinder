from collections import deque, defaultdict
import heapq
import math
import time
from .models import Node, Edge


# PathfindingAlgorithms class implements various graph search algorithms
class PathfindingAlgorithms:
    """Implementation of various pathfinding algorithms"""
    
    def __init__(self):
        # Build the graph and node dictionary from the database
        self.graph = self._build_graph()
        self.nodes_dict = {node.id: node for node in Node.objects.all()}
    
    def _build_graph(self):
        """Build adjacency list representation of the graph"""
        graph = defaultdict(list)
        edges = Edge.objects.select_related('from_node', 'to_node').all()
        
        for edge in edges:
            # Add edge from from_node to to_node
            graph[edge.from_node.id].append({
                'node_id': edge.to_node.id,
                'weight': edge.weight
            })
            # Add reverse edge for undirected graph
            graph[edge.to_node.id].append({
                'node_id': edge.from_node.id,
                'weight': edge.weight
            })
        
        return graph
    
    def _heuristic(self, node1_id, node2_id):
        """Calculate Euclidean distance between two nodes using Haversine formula"""
        node1 = self.nodes_dict[node1_id]
        node2 = self.nodes_dict[node2_id]
        
        # Convert to radians
        lat1, lon1 = math.radians(node1.latitude), math.radians(node1.longitude)
        lat2, lon2 = math.radians(node2.latitude), math.radians(node2.longitude)
        
        # Haversine formula for distance
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Earth's radius in kilometers
        return c * r
    
    def bfs(self, start_id, end_id):
        """Breadth-First Search algorithm for shortest path in unweighted graphs"""
        start_time = time.time()
        
        queue = deque([(start_id, [start_id])])  # Queue of (current_node, path)
        visited = {start_id}
        nodes_explored = 0
        
        while queue:
            current_node, path = queue.popleft()
            nodes_explored += 1
            
            if current_node == end_id:
                end_time = time.time()
                return {
                    'path': path,
                    'distance': len(path) - 1,  # Number of edges
                    'nodes_explored': nodes_explored,
                    'execution_time': (end_time - start_time) * 1000,  # milliseconds
                    'algorithm': 'BFS'
                }
            
            for neighbor in self.graph[current_node]:
                neighbor_id = neighbor['node_id']
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append((neighbor_id, path + [neighbor_id]))
        
        return None  # No path found
    
    def dfs(self, start_id, end_id):
        """Depth-First Search algorithm for pathfinding"""
        start_time = time.time()
        
        stack = [(start_id, [start_id])]  # Stack of (current_node, path)
        visited = {start_id}
        nodes_explored = 0
        
        while stack:
            current_node, path = stack.pop()
            nodes_explored += 1
            
            if current_node == end_id:
                end_time = time.time()
                return {
                    'path': path,
                    'distance': len(path) - 1,
                    'nodes_explored': nodes_explored,
                    'execution_time': (end_time - start_time) * 1000,  # milliseconds
                    'algorithm': 'DFS'
                }
            
            for neighbor in self.graph[current_node]:
                neighbor_id = neighbor['node_id']
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    stack.append((neighbor_id, path + [neighbor_id]))
        
        return None  # No path found
    
    def dijkstra(self, start_id, end_id):
        """Dijkstra's algorithm for shortest path in weighted graphs"""
        start_time = time.time()
        
        distances = defaultdict(lambda: float('inf'))  # Distance from start to each node
        distances[start_id] = 0
        previous = {}  # To reconstruct path
        heap = [(0, start_id)]  # Min-heap of (distance, node_id)
        visited = set()
        nodes_explored = 0
        
        while heap:
            current_distance, current_node = heapq.heappop(heap)
            nodes_explored += 1
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            if current_node == end_id:
                # Reconstruct path from end to start
                path = []
                node = end_id
                while node is not None:
                    path.append(node)
                    node = previous.get(node)
                path.reverse()
                
                end_time = time.time()
                return {
                    'path': path,
                    'distance': distances[end_id],
                    'nodes_explored': nodes_explored,
                    'execution_time': (end_time - start_time) * 1000,  # milliseconds
                    'algorithm': 'Dijkstra'
                }
            
            for neighbor in self.graph[current_node]:
                neighbor_id = neighbor['node_id']
                weight = neighbor['weight']
                distance = current_distance + weight
                
                if distance < distances[neighbor_id]:
                    distances[neighbor_id] = distance
                    previous[neighbor_id] = current_node
                    heapq.heappush(heap, (distance, neighbor_id))
        
        return None  # No path found
    
    def a_star(self, start_id, end_id):
        """A* algorithm for shortest path using heuristic (Haversine distance)"""
        start_time = time.time()
        
        open_set = [(0, start_id)]  # Min-heap of (f_score, node_id)
        g_score = defaultdict(lambda: float('inf'))  # Cost from start to node
        g_score[start_id] = 0
        f_score = defaultdict(lambda: float('inf'))  # Estimated total cost
        f_score[start_id] = self._heuristic(start_id, end_id)
        previous = {}
        nodes_explored = 0
        
        while open_set:
            current_f, current_node = heapq.heappop(open_set)
            nodes_explored += 1
            
            if current_node == end_id:
                # Reconstruct path from end to start
                path = []
                node = end_id
                while node is not None:
                    path.append(node)
                    node = previous.get(node)
                path.reverse()
                
                end_time = time.time()
                return {
                    'path': path,
                    'distance': g_score[end_id],
                    'nodes_explored': nodes_explored,
                    'execution_time': (end_time - start_time) * 1000,  # milliseconds
                    'algorithm': 'A*'
                }
            
            for neighbor in self.graph[current_node]:
                neighbor_id = neighbor['node_id']
                weight = neighbor['weight']
                tentative_g_score = g_score[current_node] + weight
                
                if tentative_g_score < g_score[neighbor_id]:
                    previous[neighbor_id] = current_node
                    g_score[neighbor_id] = tentative_g_score
                    f_score[neighbor_id] = tentative_g_score + self._heuristic(neighbor_id, end_id)
                    heapq.heappush(open_set, (f_score[neighbor_id], neighbor_id))
        
        return None  # No path found
    
    def find_path(self, start_id, end_id, algorithm='dijkstra'):
        """Find path using specified algorithm (bfs, dfs, dijkstra, astar)"""
        algorithms = {
            'bfs': self.bfs,
            'dfs': self.dfs,
            'dijkstra': self.dijkstra,
            'astar': self.a_star
        }
        
        if algorithm not in algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        return algorithms[algorithm](start_id, end_id) 