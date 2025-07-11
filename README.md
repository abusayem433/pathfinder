# Django Pathfinder with Google Maps

A Django-based web application that integrates Google Maps and implements various pathfinding algorithms (BFS, DFS, Dijkstra, A\*) to compute and visualize optimal paths between locations on a map.

## 🚀 Features

### Part A: Core Setup ✅

- Django project with proper structure
- Google Maps JavaScript API integration
- Interactive node selection for source and destination
- Modern, responsive web interface

### Part B: Algorithm Implementation ✅

- **Breadth-First Search (BFS)** - Unweighted shortest path
- **Depth-First Search (DFS)** - Path exploration algorithm
- **Dijkstra's Algorithm** - Weighted shortest path
- **A\* Algorithm** - Heuristic-based optimal pathfinding
- Graph representation with 41 locations across Greater Dhaka metropolitan area
- Real-time path visualization on Google Maps

### Part C: Enhancements ✅

- Algorithm selection dropdown
- Performance metrics comparison
- Side-by-side algorithm comparison
- Beautiful, modern UI with animations
- Responsive design for mobile devices

## 🏗️ Project Structure

```
pathfinder/
├── pathfinder/              # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py
├── maps/                   # Main Django app
│   ├── models.py          # Node and Edge models
│   ├── views.py           # API endpoints and views
│   ├── algorithms.py      # Pathfinding algorithms implementation
│   ├── admin.py           # Django admin interface
│   ├── urls.py            # App URL patterns
│   └── management/commands/populate_sample_data.py
├── templates/maps/
│   └── index.html         # Main web interface
├── static/
│   ├── css/style.css      # Custom styles
│   └── js/pathfinder.js   # Frontend JavaScript
├── requirements.txt       # Python dependencies
├── manage.py             # Django management script
├── QUICK_START.md        # Quick setup guide
└── README.md
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Maps API key

### 1. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Django Configuration
SECRET_KEY=django-insecure-development-key-change-in-production
DEBUG=True

# Google Maps API Key (REQUIRED!)
GOOGLE_MAPS_API_KEY=your_actual_google_maps_api_key_here
```

**⚠️ Important**: Replace `your_actual_google_maps_api_key_here` with your real Google Maps API key!

### 3. Get Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the following APIs:
   - **Maps JavaScript API**
   - Places API (optional)
4. Create credentials → **API Key**
5. Restrict the API key to your domain (for production)
6. Add the API key to your `.env` file

### 4. Database Setup

```bash
# Create database migrations
python manage.py makemigrations maps
python manage.py migrate

# Create sample data (41 Greater Dhaka locations with connections)
python manage.py populate_sample_data

# Create superuser (optional, for admin access)
python manage.py createsuperuser
```

### 5. Run the Application

```bash
# Start the development server
python manage.py runserver

# Open your browser and visit:
# http://127.0.0.1:8000/
```

## 🎮 Usage Guide

### Basic Pathfinding

1. **Select Source**: Choose starting location from dropdown
2. **Select Destination**: Choose ending location from dropdown
3. **Choose Algorithm**: Select from BFS, DFS, Dijkstra, or A\*
4. **Find Path**: Click "Find Path" to calculate and visualize the route
5. **View Results**: See path details and performance metrics

### Algorithm Comparison

1. Select source and destination nodes
2. Click "Compare All Algorithms"
3. View side-by-side performance comparison table
4. Analyze execution time, nodes explored, and path efficiency

### Map Features

- **Blue Markers**: Available nodes/locations
- **Green Marker**: Selected source node
- **Red Marker**: Selected destination node
- **Yellow Line**: Calculated optimal path
- **Gray Lines**: Available connections between nodes
- **Info Windows**: Click markers for location details

## 🧮 Algorithm Details

### Breadth-First Search (BFS)

- **Use Case**: Unweighted graphs, shortest path by number of edges
- **Time Complexity**: O(V + E)
- **Guarantees**: Shortest path in unweighted graphs

### Depth-First Search (DFS)

- **Use Case**: Graph exploration, finding any path
- **Time Complexity**: O(V + E)
- **Guarantees**: Finds a path (not necessarily shortest)

### Dijkstra's Algorithm

- **Use Case**: Weighted graphs, shortest path by total weight
- **Time Complexity**: O((V + E) log V)
- **Guarantees**: Optimal shortest path in weighted graphs

### A\* Algorithm

- **Use Case**: Weighted graphs with heuristic information
- **Time Complexity**: O(b^d) where b is branching factor, d is depth
- **Guarantees**: Optimal path with admissible heuristic
- **Heuristic**: Haversine distance formula for geographic coordinates

## 🎨 Sample Data

The application includes 41 locations across Greater Dhaka metropolitan area:

**Central Dhaka**: Shaheed Minar, University of Dhaka, Ramna Park, BUET
**Old Dhaka**: Lalbagh Fort, Ahsan Manzil, Sadarghat, Chawk Bazaar  
**Modern Commercial**: Motijheel, Farmgate, Kawran Bazar, Tejgaon
**Northern Areas**: Uttara, Airport, Mohakhali, Gulshan, Banani
**Western Suburbs**: Mirpur, Savar, Dhamrai, Jahangirnagar University
**Eastern Districts**: Badda, Rampura, Bashundhara, Cantonment
**Southern Region**: Keraniganj, Narayanganj, Munshiganj
**Educational & Cultural**: Nilkhet, Elephant Road, Dhanmondi

Connections are based on realistic geographic proximity and transportation routes with 76 total edges covering the entire metropolitan area.

## 🔧 API Endpoints

- `GET /` - Main application interface
- `POST /api/find-path/` - Calculate path between nodes
- `GET /api/nodes/` - Get all available nodes
- `GET /api/edges/` - Get all connections/edges

## 🎯 Performance Metrics

The application tracks and displays:

- **Execution Time**: Algorithm runtime in milliseconds
- **Nodes Explored**: Number of nodes visited during search
- **Path Distance**: Total weighted distance of found path
- **Path Length**: Number of edges in the optimal path

## 🚧 Troubleshooting

### Common Issues

**Maps not loading:**

- Verify Google Maps API key is correctly set in `.env` file
- Check browser console for API errors (F12 → Console)
- Ensure Maps JavaScript API is enabled in Google Cloud Console
- Make sure there are no billing issues with your Google Cloud account

**No nodes visible:**

- Run `python manage.py populate_sample_data` to create sample data
- Check database connectivity
- Verify migrations are applied with `python manage.py showmigrations`

**Path calculation errors:**

- Ensure source and destination nodes are different
- Check that nodes are connected in the graph
- Review browser console for JavaScript errors
- Verify the Django server is running

**Server won't start:**

- Check if port 8000 is already in use: `lsof -i :8000`
- Try a different port: `python manage.py runserver 8001`
- Ensure all dependencies are installed: `pip install -r requirements.txt`

## 🔄 Development

### Adding New Locations

1. Use Django admin (`/admin/`) to add nodes and edges
2. Or modify `populate_sample_data.py` for bulk additions
3. Ensure proper latitude/longitude coordinates

### Adding New Algorithms

1. Implement algorithm in `maps/algorithms.py`
2. Add to algorithm dropdown in template
3. Update frontend JavaScript handlers

## 📚 Technical Implementation

### Backend (Django)

- **Models**: Node and Edge models for graph representation
- **Algorithms**: Comprehensive pathfinding implementations
- **APIs**: RESTful endpoints for frontend communication
- **Database**: SQLite for development (easily configurable for production)

### Frontend (JavaScript)

- **Google Maps API**: Interactive map visualization
- **AJAX**: Asynchronous API communication
- **Bootstrap**: Responsive UI framework
- **Custom CSS**: Modern styling with animations

### Algorithms Architecture

- **Graph Builder**: Converts database models to adjacency list
- **Heuristic Function**: Haversine distance for A\* algorithm
- **Performance Tracking**: Execution time and node exploration metrics
- **Path Reconstruction**: Efficient backtracking for optimal paths

## 📝 License

This project is created for educational purposes. Feel free to use and modify as needed.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

**🎯 Mission Accomplished**: Complete Django pathfinding application with Google Maps integration, featuring 4 algorithms, performance comparison, and beautiful UI!

For a quick 5-minute setup, see [QUICK_START.md](QUICK_START.md)
