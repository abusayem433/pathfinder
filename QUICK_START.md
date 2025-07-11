# 🚀 Quick Start Guide

Get the Django Pathfinder application running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Internet connection for Google Maps

## Step-by-Step Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Environment File

Create a `.env` file in the project root:

```bash
# Django Configuration
SECRET_KEY=django-insecure-development-key-change-in-production
DEBUG=True

# Google Maps API Key (REQUIRED)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

### 3. Setup Database

```bash
python manage.py makemigrations maps
python manage.py migrate
python manage.py populate_sample_data
```

### 4. Run the Application

```bash
python manage.py runserver
```

### 5. Open in Browser

Visit: http://127.0.0.1:8000/

## 🗝️ Get Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable **Maps JavaScript API**
4. Create credentials → **API Key**
5. Copy the key to your `.env` file

## ✅ Verification

If everything works correctly, you should see:

- A map with 41 Greater Dhaka metropolitan area markers
- Dropdown menus to select source/destination
- Algorithm selection options
- "Find Path" button that works

## 🎯 Test the Features

1. **Basic Pathfinding:**

   - Source: Shaheed Minar
   - Destination: Lalbagh Fort
   - Algorithm: Dijkstra
   - Click "Find Path"

2. **Algorithm Comparison:**
   - Select any two locations
   - Click "Compare All Algorithms"
   - View performance metrics

## 🆘 Quick Troubleshooting

- **Maps not loading?** → Check your Google Maps API key
- **No data?** → Run `python manage.py populate_sample_data`
- **Server error?** → Check `pip install -r requirements.txt`

---

For detailed documentation, see the main [README.md](README.md)
