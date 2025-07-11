from django.core.management.base import BaseCommand
from maps.models import Node, Edge
import math


class Command(BaseCommand):
    help = 'Populate the database with sample graph nodes and edges for Dhaka, Bangladesh'

    def handle(self, *args, **options):
        # Clear existing data
        Edge.objects.all().delete()
        Node.objects.all().delete()
        
        # Create sample nodes (representing locations across Greater Dhaka, Bangladesh)
        nodes_data = [
            # Central Dhaka - Historic & Government
            {'name': 'Shaheed Minar', 'lat': 23.7280, 'lng': 90.3979, 'desc': 'National monument for Language Movement martyrs'},
            {'name': 'Lalbagh Fort', 'lat': 23.7186, 'lng': 90.3861, 'desc': 'Mughal fort complex from 17th century'},
            {'name': 'Dhakeshwari Temple', 'lat': 23.7269, 'lng': 90.3870, 'desc': 'Ancient Hindu temple, national temple of Bangladesh'},
            {'name': 'Ahsan Manzil', 'lat': 23.7085, 'lng': 90.4064, 'desc': 'Pink Palace, former residence of Nawab of Dhaka'},
            {'name': 'National Parliament House', 'lat': 23.7625, 'lng': 90.3773, 'desc': 'Jatiyo Sangsad Bhaban, designed by Louis Kahn'},
            {'name': 'University of Dhaka', 'lat': 23.7283, 'lng': 90.3932, 'desc': 'Oldest university in Bangladesh, established 1921'},
            {'name': 'Ramna Park', 'lat': 23.7384, 'lng': 90.3939, 'desc': 'Large public park in the heart of Dhaka'},
            {'name': 'Central Shaheed Minar', 'lat': 23.7275, 'lng': 90.3981, 'desc': 'Central Language Martyrs Memorial'},
            {'name': 'Bangabandhu Stadium', 'lat': 23.7286, 'lng': 90.3854, 'desc': 'National stadium of Bangladesh'},
            
            # Old Dhaka & River Areas
            {'name': 'Sadarghat', 'lat': 23.7104, 'lng': 90.4074, 'desc': 'Historic river port on Buriganga River'},
            {'name': 'Old Dhaka', 'lat': 23.7104, 'lng': 90.4074, 'desc': 'Historic old part of Dhaka city'},
            {'name': 'Wari', 'lat': 23.7196, 'lng': 90.4186, 'desc': 'Historic neighborhood with archaeological significance'},
            {'name': 'Baitul Mukarram', 'lat': 23.7263, 'lng': 90.4089, 'desc': 'National Mosque of Bangladesh'},
            {'name': 'Chawk Bazaar', 'lat': 23.7137, 'lng': 90.4053, 'desc': 'Traditional marketplace in Old Dhaka'},
            
            # Dhanmondi & Surrounding Areas
            {'name': 'Dhanmondi Lake', 'lat': 23.7465, 'lng': 90.3760, 'desc': 'Popular recreational lake in Dhanmondi area'},
            {'name': 'New Market', 'lat': 23.7335, 'lng': 90.3756, 'desc': 'Historic shopping center since 1954'},
            {'name': 'Nilkhet', 'lat': 23.7343, 'lng': 90.3697, 'desc': 'Famous book market and educational hub'},
            {'name': 'Elephant Road', 'lat': 23.7388, 'lng': 90.3897, 'desc': 'Major commercial street in central Dhaka'},
            
            # Gulshan & Diplomatic Zone
            {'name': 'Gulshan Lake', 'lat': 23.7816, 'lng': 90.4149, 'desc': 'Artificial lake in Gulshan diplomatic zone'},
            {'name': 'Gulshan 1', 'lat': 23.7808, 'lng': 90.4142, 'desc': 'Upscale residential and commercial area'},
            {'name': 'Banani', 'lat': 23.7936, 'lng': 90.4067, 'desc': 'Modern commercial and residential district'},
            
            # Business & Commercial Districts
            {'name': 'Motijheel', 'lat': 23.7337, 'lng': 90.4166, 'desc': 'Commercial and financial district'},
            {'name': 'Hatirjheel', 'lat': 23.7520, 'lng': 90.4202, 'desc': 'Urban lake and recreational area'},
            {'name': 'Farmgate', 'lat': 23.7579, 'lng': 90.3889, 'desc': 'Major commercial hub and transport junction'},
            {'name': 'Kawran Bazar', 'lat': 23.7509, 'lng': 90.3967, 'desc': 'Largest wholesale market in Bangladesh'},
            {'name': 'Tejgaon', 'lat': 23.7636, 'lng': 90.3926, 'desc': 'Industrial and commercial area'},
            
            # Northern Dhaka
            {'name': 'Uttara', 'lat': 23.8754, 'lng': 90.3804, 'desc': 'Planned residential area in northern Dhaka'},
            {'name': 'Hazrat Shahjalal Airport', 'lat': 23.8433, 'lng': 90.3978, 'desc': 'Main international airport of Bangladesh'},
            {'name': 'Mohakhali', 'lat': 23.7810, 'lng': 90.3987, 'desc': 'Business district with bus terminal'},
            {'name': 'Cantonment', 'lat': 23.8116, 'lng': 90.4233, 'desc': 'Military cantonment area'},
            
            # Western Areas
            {'name': 'Mirpur', 'lat': 23.8223, 'lng': 90.3650, 'desc': 'Large residential area in western Dhaka'},
            {'name': 'Savar', 'lat': 23.8583, 'lng': 90.2667, 'desc': 'Industrial town near Dhaka with National Memorial'},
            {'name': 'Dhamrai', 'lat': 23.9050, 'lng': 90.1333, 'desc': 'Historic town known for handicrafts'},
            
            # Eastern Areas
            {'name': 'Badda', 'lat': 23.7804, 'lng': 90.4316, 'desc': 'Residential area in eastern Dhaka'},
            {'name': 'Rampura', 'lat': 23.7623, 'lng': 90.4296, 'desc': 'Mixed residential and commercial area'},
            {'name': 'Bashundhara', 'lat': 23.8074, 'lng': 90.4304, 'desc': 'Modern planned residential area'},
            
            # Southern Areas
            {'name': 'Keraniganj', 'lat': 23.6790, 'lng': 90.3889, 'desc': 'Industrial area south of Dhaka'},
            {'name': 'Narayanganj', 'lat': 23.6147, 'lng': 90.5000, 'desc': 'Historic river port city near Dhaka'},
            {'name': 'Munshiganj', 'lat': 23.5422, 'lng': 90.5305, 'desc': 'River district southeast of Dhaka'},
            
            # Educational & Cultural Hubs
            {'name': 'BUET', 'lat': 23.7263, 'lng': 90.3925, 'desc': 'Bangladesh University of Engineering and Technology'},
            {'name': 'Jahangirnagar University', 'lat': 23.8819, 'lng': 90.2660, 'desc': 'Public university in Savar'}
        ]
        
        # Create nodes
        created_nodes = []
        for node_data in nodes_data:
            node = Node.objects.create(
                name=node_data['name'],
                latitude=node_data['lat'],
                longitude=node_data['lng'],
                description=node_data['desc']
            )
            created_nodes.append(node)
            self.stdout.write(f"Created node: {node.name}")
        
        # Helper function to calculate distance between two points
        def calculate_distance(lat1, lon1, lat2, lon2):
            """Calculate distance using Haversine formula"""
            R = 6371  # Earth's radius in kilometers
            
            lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            
            return R * c
        
        # Create edges connecting nearby nodes
        edges_created = 0
        
        # Define manual connections for a comprehensive Greater Dhaka graph
        connections = [
            # Central Dhaka Historic Core
            ('Shaheed Minar', 'University of Dhaka'),
            ('University of Dhaka', 'Dhakeshwari Temple'),
            ('Shaheed Minar', 'Central Shaheed Minar'),
            ('University of Dhaka', 'Ramna Park'),
            ('Ramna Park', 'Elephant Road'),
            ('Dhakeshwari Temple', 'Lalbagh Fort'),
            ('Bangabandhu Stadium', 'Shaheed Minar'),
            ('University of Dhaka', 'BUET'),
            
            # Old Dhaka Network
            ('Lalbagh Fort', 'Ahsan Manzil'),
            ('Ahsan Manzil', 'Sadarghat'),
            ('Sadarghat', 'Old Dhaka'),
            ('Old Dhaka', 'Wari'),
            ('Old Dhaka', 'Chawk Bazaar'),
            ('Dhakeshwari Temple', 'Old Dhaka'),
            ('Baitul Mukarram', 'Wari'),
            ('Chawk Bazaar', 'Lalbagh Fort'),
            
            # Dhanmondi & Nearby Areas
            ('New Market', 'Dhanmondi Lake'),
            ('Dhanmondi Lake', 'National Parliament House'),
            ('New Market', 'Nilkhet'),
            ('Nilkhet', 'University of Dhaka'),
            ('Elephant Road', 'New Market'),
            ('Ramna Park', 'Elephant Road'),
            
            # Business & Commercial Districts
            ('Motijheel', 'Baitul Mukarram'),
            ('Motijheel', 'Hatirjheel'),
            ('Farmgate', 'Kawran Bazar'),
            ('Kawran Bazar', 'Tejgaon'),
            ('Tejgaon', 'Ramna Park'),
            ('Farmgate', 'National Parliament House'),
            ('Elephant Road', 'Farmgate'),
            
            # Northern Dhaka Connections
            ('Hazrat Shahjalal Airport', 'Uttara'),
            ('Uttara', 'Cantonment'),
            ('Cantonment', 'Gulshan 1'),
            ('Gulshan 1', 'Gulshan Lake'),
            ('Gulshan Lake', 'Banani'),
            ('Banani', 'Mohakhali'),
            ('Mohakhali', 'Farmgate'),
            ('Tejgaon', 'Mohakhali'),
            
            # Western Area Network
            ('Mirpur', 'Savar'),
            ('Savar', 'Jahangirnagar University'),
            ('Savar', 'Dhamrai'),
            ('Mirpur', 'Farmgate'),
            ('National Parliament House', 'Mirpur'),
            
            # Eastern Area Connections
            ('Hatirjheel', 'Badda'),
            ('Badda', 'Rampura'),
            ('Rampura', 'Bashundhara'),
            ('Bashundhara', 'Cantonment'),
            ('Gulshan Lake', 'Badda'),
            ('Banani', 'Bashundhara'),
            
            # Southern Area Network
            ('Sadarghat', 'Keraniganj'),
            ('Keraniganj', 'Narayanganj'),
            ('Narayanganj', 'Munshiganj'),
            ('Motijheel', 'Keraniganj'),
            ('Wari', 'Keraniganj'),
            
            # Cross-Regional Major Connections
            ('Ramna Park', 'New Market'),
            ('University of Dhaka', 'Motijheel'),
            ('Sadarghat', 'Motijheel'),
            ('Hatirjheel', 'Ramna Park'),
            ('Dhanmondi Lake', 'Ramna Park'),
            ('Gulshan Lake', 'Hatirjheel'),
            ('National Parliament House', 'Ramna Park'),
            ('Farmgate', 'Gulshan 1'),
            ('Tejgaon', 'Badda'),
            ('Mohakhali', 'Gulshan Lake'),
            
            # Educational Connections
            ('BUET', 'Nilkhet'),
            ('Jahangirnagar University', 'University of Dhaka'),
            ('BUET', 'Elephant Road'),
            
            # Airport & Transport Hubs
            ('Hazrat Shahjalal Airport', 'Mohakhali'),
            ('Uttara', 'Mirpur'),
            ('Farmgate', 'Tejgaon'),
        ]
        
        # Create edges from the connections list
        node_dict = {node.name: node for node in created_nodes}
        
        for from_name, to_name in connections:
            from_node = node_dict[from_name]
            to_node = node_dict[to_name]
            
            # Calculate distance as weight
            distance = calculate_distance(
                from_node.latitude, from_node.longitude,
                to_node.latitude, to_node.longitude
            )
            
            # Create edge (undirected graph - we'll handle this in the algorithm)
            edge, created = Edge.objects.get_or_create(
                from_node=from_node,
                to_node=to_node,
                defaults={'weight': round(distance, 2)}
            )
            
            if created:
                edges_created += 1
                self.stdout.write(f"Created edge: {from_name} -> {to_name} (Weight: {edge.weight})")
        
        # Create some additional strategic connections to ensure full connectivity
        import random
        random.seed(42)  # For reproducible results
        
        for _ in range(12):
            node1, node2 = random.sample(created_nodes, 2)
            
            # Check if edge already exists
            if not Edge.objects.filter(from_node=node1, to_node=node2).exists() and \
               not Edge.objects.filter(from_node=node2, to_node=node1).exists():
                
                distance = calculate_distance(
                    node1.latitude, node1.longitude,
                    node2.latitude, node2.longitude
                )
                
                # Only add if distance is reasonable (less than 25km for Greater Dhaka)
                if distance < 25:
                    edge = Edge.objects.create(
                        from_node=node1,
                        to_node=node2,
                        weight=round(distance, 2)
                    )
                    edges_created += 1
                    self.stdout.write(f"Created random edge: {node1.name} -> {node2.name} (Weight: {edge.weight})")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(created_nodes)} nodes and {edges_created} edges for Greater Dhaka, Bangladesh!')
        ) 