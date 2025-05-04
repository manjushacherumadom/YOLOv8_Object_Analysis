#app.py

import os
import sys
import cv2
import numpy as np
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_file
from app import detector
#import detector
from app.detector import ObjectTracker

STATIC_FOLDER = os.path.join(os.path.dirname(__file__), "static")
app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path="/static")
UPLOAD_FOLDER = "uploads"



os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed video formats
ALLOWED_EXTENSIONS = {"mp4", "avi", "mov", "mkv"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["TESTING"] = True

tracker = ObjectTracker()

def allowed_file(filename):
    """ Check if file format is allowed """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_video():
    """ Convert the processed video to a browser-friendly format using FFmpeg """
    print("reached convert process")
    input_path = os.path.join(STATIC_FOLDER, "output.mp4")
    output_path = os.path.join(STATIC_FOLDER, "converted_output.mp4")

    # **Check if processed video exists before converting**
    if not os.path.exists(input_path):
        print("[ERROR] output.mp4 not found. Video processing may have failed.")
        return None

    print("[INFO] Converting processed video to browser-friendly format...")
    
    subprocess.run(["ffmpeg", "-y", "-i", input_path, "-vf", "scale=640:-1",
                    "-c:v", "libx264", "-crf", "23", "-preset", "fast",
                    "-c:a", "aac", "-b:a", "128k", output_path], check=True)
    return "converted_output.mp4"

@app.route("/", methods=["GET", "POST"])
def upload_video():
    """ Handle video upload and processing """
    if request.method == "POST":
        file = request.files["video"]
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            print("video upload success")
            file.save(filepath)

            # Process video and ensure it was successfully saved
            processed_video = tracker.process_video(filepath)
            full_path = os.path.abspath(os.path.join(STATIC_FOLDER, "output.mp4"))
            print(f"[DEBUG] Checking file existence at: {full_path}")
            print(f"[DEBUG] File exists: {os.path.exists(full_path)}")
            if processed_video and os.path.exists(os.path.join(STATIC_FOLDER, "output.mp4")):
                print("output.mp4 processing")
                converted_filename = convert_video()
                if converted_filename:
                    return redirect(url_for("view_results", filename=converted_filename))
            else:
                print("[ERROR] Video processing failed—output.mp4 was not created.")
                return render_template("error.html", message="Video processing failed. Please try again.")

    return render_template("index.html")

@app.route("/results")
def view_results():
    """ Display results with the converted video """
    return render_template("results.html", filename="converted_output.mp4")

@app.route("/static/<path:filename>")
def serve_static(filename):
    """ Serve converted video file dynamically """
    return send_file(os.path.join(STATIC_FOLDER, filename), mimetype="video/mp4", conditional=False)

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000)
