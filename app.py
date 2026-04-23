from flask import Flask, jsonify, render_template
import datetime
import platform
import os

app = Flask(__name__)

def get_system_info():
    """Returns system and app information."""
    return {
        "app_name": "DevOps CI/CD Dashboard 🚀",
        "version": os.environ.get("APP_VERSION", "1.0.0"),
        "environment": os.environ.get("FLASK_ENV", "production"),
        "python_version": platform.python_version(),
        "platform": platform.system(),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }

def get_pipeline_stages():
    """Returns the CI/CD pipeline stages definition."""
    return [
        {"id": 1, "name": "Source",      "icon": "⬡", "status": "success", "description": "Push to GitHub"},
        {"id": 2, "name": "Install",     "icon": "⬡", "status": "success", "description": "pip install dependencies"},
        {"id": 3, "name": "Test",        "icon": "⬡", "status": "success", "description": "pytest unit tests"},
        {"id": 4, "name": "Build",       "icon": "⬡", "status": "success", "description": "docker build image"},
        {"id": 5, "name": "Push",        "icon": "⬡", "status": "success", "description": "Push to Docker Hub"},
        {"id": 6, "name": "Deploy",      "icon": "⬡", "status": "success", "description": "Live on Render.com"},
    ]

@app.route("/")
def index():
    info = get_system_info()
    stages = get_pipeline_stages()
    return render_template("index.html", info=info, stages=stages)

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "message": "App is running healthy ✅"})

@app.route("/api/info")
def info():
    return jsonify(get_system_info())

@app.route("/api/pipeline")
def pipeline():
    return jsonify(get_pipeline_stages())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
