import cv2
import numpy as np
import time
import os
import scipy.spatial
import scipy.optimize
from ultralytics import YOLO

class ObjectTracker:
    def __init__(self):
        # Load YOLOv8 model
        self.model = YOLO("yolov8n.pt")

        # Object tracking variables
        self.tracked_objects = {}  # Stores object positions & timestamps
        self.tracked_ids = {}  # Persistent ID storage
        self.entry_count = 0
        self.exit_count = 0
        self.speed_buffer = {}  # Store past speeds for smoothing

        # Line coordinates for speed estimation (middle of frame)
        #self.line_y_position = int(frame_height * 0.5)  # Adjust based on input video
        self.previous_positions = {}

        # Video writer setup
        #output_path = "app/static/output.mp4"
        #self.frame_width = 680  # Set based on video dimensions
        #self.frame_height = 384  # Set based on video dimensions

        #fourcc = cv2.VideoWriter_fourcc(*"XVID")
        #self.out_writer = cv2.VideoWriter(self.output_path, fourcc, 30, (self.frame_width, self.frame_height))


        # Global counting variables
        self.global_count = 0  # Track total detected objects
        self.region_counts = {"Entry Zone": 0, "Middle Zone": 0, "Exit Zone": 0}  # Store region-wise counts

        


    def match_objects(self, prev_positions, current_detections):
        """ Use Hungarian algorithm to stabilize object tracking IDs. """
        #matched_ids = self.match_objects(prev_positions, detections)
        matched_ids = {}  # Initialize empty dictionary
        prev_keys = np.array(list(prev_positions.keys()))
        current_keys = np.array([list(det[:4]) for det in current_detections])

        if prev_keys.size == 0 or current_keys.size == 0:  # Handle empty cases
            return {}

        prev_keys = prev_keys.reshape(-1, 4)
        current_keys = current_keys.reshape(-1, 4)

        # Compute distance matrix between previous and current detections
        distance_matrix = scipy.spatial.distance.cdist(prev_keys, current_keys, metric="euclidean")
        row_idx, col_idx = scipy.optimize.linear_sum_assignment(distance_matrix)

        matched_objects = {}
        for r, c in zip(row_idx, col_idx):
            matched_objects[tuple(current_keys[c])] = prev_positions[tuple(prev_keys[r])]

        return matched_objects

    def process_video(self, video_path):
        """ Detect, track, count objects & estimate speed in a video. """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("[ERROR] Cannot open video file!")
            return None

        prev_frame = None
        previous_positions = {}
        speed_buffer = {}
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        frame_width, frame_height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.line_y_position = int(frame_height * 0.5)  # Adjust based on input video
        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Changed codec for better compatibility
        output_path = "app/static/output.mp4"

        print(f"[INFO] Saving video to: {output_path}")

        out_writer = cv2.VideoWriter(output_path, fourcc, frame_rate, (frame_width, frame_height))

        prev_positions = {}

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            results = self.model.track(source=frame, tracker="bytetrack.yaml", conf=0.5)
            detections = results[0].boxes.data.cpu().numpy()
            matched_ids = self.match_objects(prev_positions, detections)
            # Draw reference line for speed estimation
            cv2.line(frame, (0, self.line_y_position), (frame_width, self.line_y_position), (0, 0, 255), 2)

            self.region_counts = {"Entry Zone": 0, "Middle Zone": 0, "Exit Zone": 0}

            for det in detections:
                x1, y1, x2, y2, conf, cls = det[:6]
                obj_key = tuple(det[:4])
                
                # Keep IDs consistent across frames
                if obj_key in matched_ids:
                    track_id = matched_ids[obj_key]
                else:
                    track_id = self.tracked_ids.get(obj_key, np.random.randint(10, 99))

                #track_id = self.tracked_ids.get(obj_key, np.random.randint(10, 99))

                
                self.tracked_ids[obj_key] = track_id

                # Speed estimation
                       
                METERS_PER_PIXEL = 0.5  # Conversion factor for real-world speed

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                current_time = time.time()
                x, y, w, h = None, None, None, None  # Default values
                if prev_frame is not None:
                    
                    diff = cv2.absdiff(prev_frame, gray)
                    _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
                    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    for cnt in contours:
                        if cv2.contourArea(cnt) > 500:
                            x, y, w, h = cv2.boundingRect(cnt)
                            track_id = hash((x, y))  # Generating a simple tracking ID
                            current_time = time.time()
                            position = (x + w // 2, y + h // 2)
                
                            prev_position = previous_positions.get(track_id, None)
                            previous_positions[track_id] = (position[0], position[1], current_time)

                            if prev_position is not None:
                                prev_x, prev_y, prev_time = prev_position

                                pixel_distance = ((position[0] - prev_x) ** 2 + (position[1] - prev_y) ** 2) ** 0.5
                                real_distance = pixel_distance * METERS_PER_PIXEL

                                time_diff = max(current_time - prev_time, 0.1)

                                persisted_speeds = {}
                                if time_diff > 0:
                                    speed_mps = real_distance / time_diff
                                    speed_kmph = speed_mps * 3.6
                                    speed_kmph = min(speed_kmph, 120)  # Limit speed estimates

                                    speed_buffer[track_id] = speed_buffer.get(track_id, [])[-5:]
                                    speed_buffer[track_id].append(speed_kmph)

                                    avg_speed_kmph = sum(speed_buffer[track_id]) / len(speed_buffer[track_id])
                                    # Persist the last known speed for each vehicle
                                    persisted_speeds[track_id] = avg_speed_kmph
                                    print(f"[DEBUG] Speed calculated: {speed_kmph:.2f} km/h for ID {track_id}")
                                    
                                    # Display persisted speed even if no update occurs
                                    if track_id in persisted_speeds:
                                        cv2.putText(frame, f"Speed: {avg_speed_kmph:.1f} km/h", (int(position[0]), int(position[1]) - 30),
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

                                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                

                prev_frame = gray.copy()
                #cv2.imshow("Frame", frame)

                 
               

                self.previous_positions[track_id] = (x1, y1, current_time)


                # Count objects in regions
                if y1 < 100:
                    self.region_counts["Entry Zone"] += 1
                elif 100 <= y1 < 400:
                    self.region_counts["Middle Zone"] += 1
                elif y1 >= 400:
                    self.region_counts["Exit Zone"] += 1
                self.global_count += 1  # Track overall count

                # Draw bounding box & tracking ID
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, f"ID {track_id}", (int(x1), int(y1) - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

                # Overlay global & region-wise counts
                cv2.rectangle(frame, (5, 10), (250, 100), (255, 255, 255), -1)
                cv2.putText(frame, f"Total Count: {self.global_count}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
                for idx, (region, count) in enumerate(self.region_counts.items()):
                    cv2.putText(frame, f"{region}: {count}", (10, 60 + (idx * 30)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 3)

                prev_positions = {tuple(det[:4]): track_id for det in detections}
            print("[DEBUG] Attempting to write frame to output.mp4")
            out_writer.write(frame)
            print("[DEBUG] Frame successfully written to output.mp4")
            

        cap.release()
        out_writer.release()
        cv2.destroyAllWindows()

        if out_writer is not None:
            out_writer.release()
            print(f"[INFO] Processed video saved: {output_path}")
            print("[INFO] Video writer released successfully.")
        return output_path


        if not os.path.exists(output_path):
            print("[ERROR] output.mp4 was not created successfully!")
            return None

        print(f"[INFO] Processed video saved: {output_path}")
        return output_path