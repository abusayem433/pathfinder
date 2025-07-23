# Django Pathfinder

A web application for visualizing and comparing pathfinding algorithms (BFS, DFS, Dijkstra, A\*) on a map of Dhaka, Bangladesh using Django and Google Maps.

## Features

- Visualize nodes and edges on Google Maps
- Find shortest paths using multiple algorithms
- Compare algorithm performance

## Explore Online

You can directly explore the live demo of this project here:

👉 [https://pathfinder.abusayem.me/](https://pathfinder.abusayem.me/)

No setup required—just visit the link and try out the pathfinding features in your browser!

## Public Repository

You can also view the full source code, report issues, or contribute to this project on GitHub:

👉 [https://github.com/abusayem433/pathfinder](https://github.com/abusayem433/pathfinder)

## Setup Instructions

1. **Open a terminal and navigate to the project folder:**
   (For example, if you received the folder and placed it on your Desktop)

   ```bash
   cd ~/Desktop/pathfinder
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   - Create a `.env` file in the project root with the following (replace with your own values):
     ```env
     SECRET_KEY=your-django-secret-key
     DEBUG=True
     GOOGLE_MAPS_API_KEY=your-google-maps-api-key
     ```

5. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Populate sample data:**

   ```bash
   python manage.py populate_sample_data
   ```

7. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

8. **Open your browser:**
   Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Opening and Running the Project in Visual Studio Code

1. **Open Visual Studio Code.**

2. **Open the project folder:**

   - Click on `File` > `Open Folder...` (or `Open...` on Mac) in the menu.
   - Browse to the location where you saved the `pathfinder` folder and select it.
   - Click `Open`.

3. **Open the integrated terminal in VS Code:**

   - Go to `View` > `Terminal` (or press <kbd>Ctrl</kbd>+<kbd>`</kbd> on Windows/Linux, <kbd>Cmd</kbd>+<kbd>`</kbd> on Mac).
   - The terminal will open at the bottom of VS Code, starting in your project directory.

4. **(Optional) Create and activate a virtual environment in the terminal:**

   - If you haven't already:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

5. **Install dependencies (if not done):**

   ```bash
   pip install -r requirements.txt
   ```

6. **Run Django commands as usual in the terminal:**

   - For example:
     ```bash
     python manage.py runserver
     ```

7. **Recommended VS Code Extensions:**

   - Python (by Microsoft)
   - Django (by Baptiste Darthenay or similar)
   - dotenv (for .env file support)

8. **Debugging:**
   - You can set breakpoints and debug Django code using the built-in VS Code debugger. Make sure the Python extension is installed.

## Notes

- Requires Python 3.8+
- Google Maps API key is needed for map display
- For production, set `DEBUG=False` and configure allowed hosts and static files

---
