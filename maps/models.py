from django.db import models


class Node(models.Model):
    """Represents a node in the graph"""
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Edge(models.Model):
    """Represents an edge between two nodes"""
    from_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='outgoing_edges')
    to_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='incoming_edges')
    weight = models.FloatField(default=1.0)  # Distance or cost
    
    def __str__(self):
        return f"{self.from_node.name} -> {self.to_node.name} (Weight: {self.weight})"
    
    class Meta:
        unique_together = ['from_node', 'to_node'] 