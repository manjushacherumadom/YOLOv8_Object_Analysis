# YOLOv8_Object_Analysis
A real-time system for detecting, tracking, counting, and analyzing object movement

Objective
To develop a real-time system for detecting, tracking, counting, and analyzing object movement in surveillance footage using YOLOv8. The system should be capable of region-based counting and estimating object speed, and deployed as a Flask-based web app containerized with Docker.

Here's a ready-to-use GitHub README for your **Object Detection and Speed Estimation** project using Flask and Docker. You can copy and paste it directly:

---

# YOLOv8 Object Analysis

## Overview
YOLOv8_Object_Analysis is a project designed for **object detection and speed estimation** using YOLOv8, Flask, and Docker. The web interface allows users to upload images and detect objects with YOLOv8.Project scope is to focus on objects such as pedestrians, vehicles, or bicycles in outdoor or indoor environments and detect them , estimate their speed and assign unique id’s to each detected object.

## Directory Structure
```
YOLOv8_Object_Analysis
├── app                     # Main application logic
│   ├── static              # Stores CSS, JS, and images
│   ├── templates           # HTML templates for UI
│   ├── uploads             # Folder for storing uploaded images
│   ├── app.py              # Entry point for the Flask app
│   ├── detector.py         # Object detection functionality
│   └── __init__.py         # Package initializer
├── models                  # YOLOv8 models and configurations
│   ├── yolov8_model.pt     # YOLOv8 model file
│   └── config.yaml         # Configuration file
├── tests                   # Unit tests for validation
│   ├── test_app.py         # Tests for Flask app functionality
│   └── test_detector.py    # Tests for object detection functions
├── uploads                 # Separate folder for storing uploaded files
├── Dockerfile              # Docker configuration
├── .dockerignore           # Files ignored by Docker builds
├── requirements.txt        # Dependencies needed for the project
└── README.md               # Documentation file
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/YOLOv8_Object_Analysis.git
   cd YOLOv8_Object_Analysis
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Docker:
   ```bash
   docker build -t yolov8_object_analysis .
   docker run -p 5000:5000 yolov8_object_analysis
   ```

## Usage

1. Start the Flask application:
   ```bash
   python app/app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`.

3. Upload an image and perform object detection.

## Testing

Run unit tests to validate the functionality:
```bash
pytest tests/
```

## Contributing

Feel free to submit issues and pull requests to improve the project.

## License

This project is licensed under the **MIT License**.

---


