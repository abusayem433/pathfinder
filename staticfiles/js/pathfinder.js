// Global variables
let map;
let nodes = [];
let edges = [];
let markers = [];
let pathPolyline = null;
let edgePolylines = [];

// Algorithm descriptions
const algorithmDescriptions = {
    'bfs': 'BFS explores nodes level by level, guaranteeing the shortest path in unweighted graphs.',
    'dfs': 'DFS explores as far as possible along each branch before backtracking.',
    'dijkstra': "Dijkstra's algorithm finds the shortest path considering edge weights.",
    'astar': 'A* uses heuristics to find the optimal path more efficiently than Dijkstra.'
};

// Initialize Google Maps
function initMap() {
    console.log('🚀 initMap called - Google Maps loading...');
    
    // Center map on Dhaka, Bangladesh
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: { lat: 23.7280, lng: 90.3979 }, // Dhaka, Bangladesh (Shaheed Minar)
        mapTypeId: 'roadmap',
        styles: [
            {
                featureType: 'poi',
                elementType: 'labels',
                stylers: [{ visibility: 'off' }]
            }
        ]
    });

    console.log('✅ Google Maps created successfully');

    // Load nodes and edges
    loadNodesAndEdges();
    
    // Initialize event listeners
    initializeEventListeners();
    
    console.log('🎯 Map initialization complete');
}

// Load nodes and edges from the backend
async function loadNodesAndEdges() {
    try {
        // Load nodes
        const nodesResponse = await fetch('/api/nodes/');
        const nodesData = await nodesResponse.json();
        nodes = nodesData.nodes;
        
        // Load edges
        const edgesResponse = await fetch('/api/edges/');
        const edgesData = await edgesResponse.json();
        edges = edgesData.edges;
        
        // Display nodes and edges on map
        displayNodesOnMap();
        displayEdgesOnMap();
        
        // Adjust map bounds to fit all nodes
        adjustMapBounds();
        
    } catch (error) {
        console.error('Error loading nodes and edges:', error);
        showAlert('Error loading map data', 'danger');
    }
}

// Display nodes as markers on the map
function displayNodesOnMap() {
    nodes.forEach(node => {
        const marker = new google.maps.Marker({
            position: { lat: node.latitude, lng: node.longitude },
            map: map,
            title: node.name,
            icon: {
                url: 'https://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                scaledSize: new google.maps.Size(32, 32)
            }
        });
        
        // Add info window
        const infoWindow = new google.maps.InfoWindow({
            content: `
                <div>
                    <h6>${node.name}</h6>
                    <p><small>${node.description || 'No description available'}</small></p>
                    <p><small>Coordinates: ${node.latitude.toFixed(4)}, ${node.longitude.toFixed(4)}</small></p>
                </div>
            `
        });
        
        marker.addListener('click', () => {
            infoWindow.open(map, marker);
        });
        
        markers.push({ marker, node });
    });
}

// Display edges as polylines on the map
function displayEdgesOnMap() {
    edges.forEach(edge => {
        const path = [
            { lat: edge.from_node.latitude, lng: edge.from_node.longitude },
            { lat: edge.to_node.latitude, lng: edge.to_node.longitude }
        ];
        
        const polyline = new google.maps.Polyline({
            path: path,
            geodesic: true,
            strokeColor: '#9e9e9e',
            strokeOpacity: 0.6,
            strokeWeight: 2
        });
        
        polyline.setMap(map);
        edgePolylines.push(polyline);
    });
}

// Adjust map bounds to fit all nodes
function adjustMapBounds() {
    if (nodes.length === 0) return;
    
    const bounds = new google.maps.LatLngBounds();
    nodes.forEach(node => {
        bounds.extend(new google.maps.LatLng(node.latitude, node.longitude));
    });
    
    map.fitBounds(bounds);
    
    // Ensure minimum zoom level
    google.maps.event.addListenerOnce(map, 'bounds_changed', () => {
        if (map.getZoom() > 15) {
            map.setZoom(15);
        }
    });
}

// Initialize event listeners
function initializeEventListeners() {
    console.log('🔧 Setting up event listeners...');
    
    // Algorithm selection change
    document.getElementById('algorithm').addEventListener('change', function() {
        const algorithm = this.value;
        document.getElementById('algorithmInfo').textContent = algorithmDescriptions[algorithm];
    });
    
    // Find path button
    document.getElementById('findPathBtn').addEventListener('click', findPath);
    console.log('✅ Find Path button listener added');
    
    // Clear path button
    document.getElementById('clearPathBtn').addEventListener('click', clearPath);
    
    // Compare algorithms button
    document.getElementById('compareAlgorithmsBtn').addEventListener('click', compareAlgorithms);
    
    console.log('✅ All event listeners initialized');
}

// Find path using selected algorithm
async function findPath() {
    console.log('🔍 Find Path button clicked!');
    
    const startId = document.getElementById('startNode').value;
    const endId = document.getElementById('endNode').value;
    const algorithm = document.getElementById('algorithm').value;
    
    console.log('📊 Selected values:', { startId, endId, algorithm });
    
    if (!startId || !endId) {
        console.log('⚠️ Missing source or destination');
        showAlert('Please select both source and destination nodes', 'warning');
        return;
    }
    
    if (startId === endId) {
        showAlert('Source and destination nodes must be different', 'warning');
        return;
    }
    
    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('findPathBtn').disabled = true;
    
    try {
        const response = await (window.fetchWithCSRF || fetch)('/api/find-path/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                start_id: parseInt(startId),
                end_id: parseInt(endId),
                algorithm: algorithm
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayPath(data);
            showResults(data);
            showAlert('Path found successfully!', 'success');
        } else {
            showAlert(data.error, 'danger');
        }
        
    } catch (error) {
        console.error('Error finding path:', error);
        showAlert('Error occurred while finding path', 'danger');
    } finally {
        // Hide loading
        document.getElementById('loading').style.display = 'none';
        document.getElementById('findPathBtn').disabled = false;
    }
}

// Display path on the map
function displayPath(data) {
    // Clear previous path
    clearPath();
    
    // Update marker colors for start and end nodes
    updateMarkerColors(data.path_ids[0], data.path_ids[data.path_ids.length - 1]);
    
    // Create path polyline
    const pathCoordinates = data.path.map(node => ({
        lat: node.latitude,
        lng: node.longitude
    }));
    
    pathPolyline = new google.maps.Polyline({
        path: pathCoordinates,
        geodesic: true,
        strokeColor: '#fbbc05',
        strokeOpacity: 1.0,
        strokeWeight: 5
    });
    
    pathPolyline.setMap(map);
    
    // Add markers for intermediate nodes in the path
    data.path.forEach((node, index) => {
        if (index > 0 && index < data.path.length - 1) {
            const marker = new google.maps.Marker({
                position: { lat: node.latitude, lng: node.longitude },
                map: map,
                title: `Path Node ${index}: ${node.name}`,
                icon: {
                    url: 'https://maps.google.com/mapfiles/ms/icons/yellow-dot.png',
                    scaledSize: new google.maps.Size(24, 24)
                }
            });
        }
    });
}

// Update marker colors for start and end nodes
function updateMarkerColors(startId, endId) {
    markers.forEach(({ marker, node }) => {
        if (node.id === startId) {
            marker.setIcon({
                url: 'https://maps.google.com/mapfiles/ms/icons/green-dot.png',
                scaledSize: new google.maps.Size(32, 32)
            });
        } else if (node.id === endId) {
            marker.setIcon({
                url: 'https://maps.google.com/mapfiles/ms/icons/red-dot.png',
                scaledSize: new google.maps.Size(32, 32)
            });
        } else {
            marker.setIcon({
                url: 'https://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                scaledSize: new google.maps.Size(32, 32)
            });
        }
    });
}

// Show path results
function showResults(data) {
    const resultsPanel = document.getElementById('resultsPanel');
    const pathInfo = document.getElementById('pathInfo');
    const metricsInfo = document.getElementById('metricsInfo');
    
    // Path information
    const pathNodes = data.path.map(node => node.name).join(' → ');
    pathInfo.innerHTML = `
        <p><strong>Algorithm:</strong> ${data.algorithm}</p>
        <p><strong>Path:</strong> ${pathNodes}</p>
        <p><strong>Total Distance:</strong> ${data.distance.toFixed(2)} units</p>
        <p><strong>Number of Nodes:</strong> ${data.path.length}</p>
    `;
    
    // Performance metrics
    metricsInfo.innerHTML = `
        <p><strong>Nodes Explored:</strong> ${data.nodes_explored}</p>
        <p><strong>Execution Time:</strong> ${data.execution_time.toFixed(2)} ms</p>
        <p><strong>Path Length:</strong> ${data.path.length - 1} edges</p>
    `;
    
    resultsPanel.style.display = 'block';
}

// Compare all algorithms
async function compareAlgorithms() {
    const startId = document.getElementById('startNode').value;
    const endId = document.getElementById('endNode').value;
    
    if (!startId || !endId) {
        showAlert('Please select both source and destination nodes for comparison', 'warning');
        return;
    }
    
    if (startId === endId) {
        showAlert('Source and destination nodes must be different', 'warning');
        return;
    }
    
    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('compareAlgorithmsBtn').disabled = true;
    
    const algorithms = ['bfs', 'dfs', 'dijkstra', 'astar'];
    const results = [];
    
    try {
        for (const algorithm of algorithms) {
            const response = await (window.fetchWithCSRF || fetch)('/api/find-path/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    start_id: parseInt(startId),
                    end_id: parseInt(endId),
                    algorithm: algorithm
                })
            });
            
            const data = await response.json();
            if (data.success) {
                results.push(data);
            }
        }
        
        displayComparison(results);
        showAlert('Algorithm comparison completed!', 'info');
        
    } catch (error) {
        console.error('Error comparing algorithms:', error);
        showAlert('Error occurred during comparison', 'danger');
    } finally {
        // Hide loading
        document.getElementById('loading').style.display = 'none';
        document.getElementById('compareAlgorithmsBtn').disabled = false;
    }
}

// Display algorithm comparison results
function displayComparison(results) {
    const comparisonPanel = document.getElementById('comparisonPanel');
    const comparisonResults = document.getElementById('comparisonResults');
    
    let tableHTML = `
        <table class="table table-striped comparison-table">
            <thead>
                <tr>
                    <th>Algorithm</th>
                    <th>Distance</th>
                    <th>Execution Time (ms)</th>
                    <th>Nodes Explored</th>
                    <th>Path Length</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    results.forEach(result => {
        tableHTML += `
            <tr>
                <td><strong>${result.algorithm}</strong></td>
                <td>${result.distance.toFixed(2)}</td>
                <td>${result.execution_time.toFixed(2)}</td>
                <td>${result.nodes_explored}</td>
                <td>${result.path.length - 1}</td>
            </tr>
        `;
    });
    
    tableHTML += `
            </tbody>
        </table>
    `;
    
    comparisonResults.innerHTML = tableHTML;
    comparisonPanel.style.display = 'block';
}

// Clear path from map
function clearPath() {
    if (pathPolyline) {
        pathPolyline.setMap(null);
        pathPolyline = null;
    }
    
    // Reset marker colors
    markers.forEach(({ marker }) => {
        marker.setIcon({
            url: 'https://maps.google.com/mapfiles/ms/icons/blue-dot.png',
            scaledSize: new google.maps.Size(32, 32)
        });
    });
    
    // Hide results panels
    document.getElementById('resultsPanel').style.display = 'none';
    document.getElementById('comparisonPanel').style.display = 'none';
}

// Show alert messages
function showAlert(message, type) {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the page
    document.querySelector('.container-fluid').insertBefore(alertDiv, document.querySelector('.row'));
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
} 