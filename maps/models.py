from django.db import models


# Node model represents a location or point in the graph
class Node(models.Model):
    """Represents a node in the graph"""
    name = models.CharField(max_length=100)  # Name of the node/location
    latitude = models.FloatField()           # Latitude coordinate
    longitude = models.FloatField()          # Longitude coordinate
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']  # Order nodes by name by default


# Edge model represents a connection between two nodes
class Edge(models.Model):
    """Represents an edge between two nodes"""
    from_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='outgoing_edges')  # Start node
    to_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='incoming_edges')    # End node
    weight = models.FloatField(default=1.0)  # Distance or cost of the edge
    
    def __str__(self):
        return f"{self.from_node.name} -> {self.to_node.name} (Weight: {self.weight})"
    
    class Meta:
        unique_together = ['from_node', 'to_node']  # Each edge is unique by its node pair 