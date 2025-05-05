# YOLOv8_Object_Analysis
A real-time system for detecting, tracking, counting, and analyzing object movement

Objective
To develop a real-time system for detecting, tracking, counting, and analyzing object movement in surveillance footage using YOLOv8. The system should be capable of region-based counting and estimating object speed, and deployed as a Flask-based web app containerized with Docker.

![image](https://github.com/user-attachments/assets/7a4ab571-d6e4-4f38-884e-d9506a3e2d67)


📂 YOLOv8_Object_Analysis
├── 📁 app                # Main application logic
│   ├── 📁 static        # Stores CSS, JS, and images
│   ├── 📁 templates     # HTML templates for UI
│   ├── 📁 uploads       # Folder for storing uploaded images
│   ├── 📄 app.py        # Entry point for the Flask app
│   ├── 📄 detector.py   # Object detection functionality
│   ├── 📄 __init__.py   # Package initializer
├── 📁 models             # YOLOv8 models and configurations
│   ├── 📄 yolov8_model.pt
│   ├── 📄 config.yaml
├── 📁 tests              # Unit tests for validation
│   ├── 📄 test_app.py    # Tests for Flask app functionality
│   ├── 📄 test_detector.py # Tests for object detection functions
├── 📁 uploads            # Separate folder for storing uploaded files
├── 📄 Dockerfile         # Docker configuration
├── 📄 .dockerignore      # Files ignored by Docker builds
├── 📄 .requirements.txt  # Dependencies needed for the project
├── 📄 README.md          # Documentation file

Project scope is to focus on objects such as pedestrians, vehicles, or bicycles in outdoor or indoor environments and detect them , estimate their speed and assign unique id’s to each detected object.

Load the YOLOv8 Model
•	The tracker initializes YOLO("yolov8n.pt") to detect objects in each frame.
•	yolov8n.pt is a lightweight YOLOv8 variant optimized for real-time inference.
self.model = YOLO("yolov8n.pt")

First, it retrieves detected objects from YOLOv8 and converts them into a NumPy format for easier processing. To ensure that objects maintain the same ID across frames, it matches detected objects with previously recorded positions using the match_objects function. This prevents misidentifications and allows objects to be consistently tracked.

Bounding boxes are drawn around detected objects using OpenCV’s cv2.rectangle(), giving a visual representation of tracked entities. Additionally, each object is labeled with a tracking ID, ensuring consistency across frames. The tracking ID is shortened for display purposes using str(track_id)[-2:].

Our code is managing video upload, processing, and conversion within a Flask-based system. First, when a user uploads a video, the file is saved to a designated upload folder. A confirmation message is printed to indicate that the upload was successful. Once stored, the tracker.process_video(filepath) function is called to analyze and process the video.

Our code is managing video upload, processing, and conversion within a Flask-based system. First, when a user uploads a video, the file is saved to a designated upload folder. A confirmation message is printed to indicate that the upload was successful. Once stored, the tracker.process_video(filepath) function is called to analyze and process the video.

In our YOLOv8 Object Analysis project, a Dockerfile defines how the container is built, specifying dependencies and configurations. The base image is Python 3.10, providing a stable environment for running your Flask application. Additional dependencies like ffmpeg and OpenGL libraries (libgl1-mesa-glx) are installed to support image and video processing. The WORKDIR command sets the /app directory as the working location inside the container. Your project files, including the Flask app (app.py), are copied into the container using the COPY command. The container exposes port 5000, allowing external access to the web application. When the container runs, the CMD command starts the Flask server automatically. You can build the image using docker build and then deploy it using docker run, mapping ports for access


Additionally, the /static/<path:filename> route serves video files directly from the static folder, allowing users to access the processed video via a browser request. The send_file function ensures that the video is delivered with the correct MIME type (video/mp4), making it compatible with most media players.
Finally, the application runs on 0.0.0.0:5000, making it accessible from any connected device within the network. If you're testing locally, you can navigate to http://localhost:5000/results to view the converted video

