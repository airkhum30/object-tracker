import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # Load once globally

# def process_frame(frame):
#     results = model(frame)
#     if isinstance(results, list):
#         results = results[0]

#     boxes = results.boxes
#     coordinates = boxes.data.cpu().numpy()

#     detections = []
#     for coordinate in coordinates:
#         x_min, y_min, x_max, y_max, confidence, class_id = coordinate
#         detections.append([int(class_id), round(confidence, 2), int(x_min), int(y_min), int(x_max), int(y_max)])
#         cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (255, 0, 0), 2)
#         cv2.putText(frame, f'{int(class_id)} {round(confidence, 2)}', (int(x_min), int(y_min) - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

#     return frame, detections

# Define the confidence threshold and class filters (optional)
CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for detection to be considered
FILTER_CLASSES = [0, 2, 3]  # Example: [0] for person, [2] for car, [3] for bike

def process_frame(frame):
    detections = []
    results = model(frame)

    if isinstance(results, list):
        results = results[0]

    boxes = results.boxes
    if boxes is None:
        return frame, detections  # Return original frame if no detections

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())  # Get box coordinates
        conf = float(box.conf[0])  # Get confidence score
        cls = int(box.cls[0])  # Get class ID
        
        # Filter by confidence and class
        if conf >= CONFIDENCE_THRESHOLD and (not FILTER_CLASSES or cls in FILTER_CLASSES):
            label = f"{model.names[cls]} {conf:.2f}"

            # Draw bounding box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Add detection (class_id, confidence, x1, y1, x2, y2)
            detections.append((cls, conf, x1, y1, x2, y2))

    return frame, detections





def process_video(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)
    tracker = sort.Sort()
    object_speed = {}
    object_counter = 0
    frame_number = 0

    # Count region
    count_region_top = 200
    count_region_bottom = 300

    os.makedirs(output_folder, exist_ok=True)
    output_csv = os.path.join(output_folder, 'tracking_results.csv')

    # Get video properties for writing
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    output_video_path = os.path.join(output_folder, 'tracked_' + os.path.basename(video_path))
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    with open(output_csv, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Frame', 'Track ID', 'X1', 'Y1', 'X2', 'Y2', 'Speed (px/s)'])

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_number += 1
            results = model(frame)
            if isinstance(results, list):
                results = results[0]

            boxes = results.boxes
            coordinates = boxes.data.cpu().numpy()

            detections = []
            for coordinate in coordinates:
                x_min, y_min, x_max, y_max, confidence, class_id = coordinate
                detections.append([x_min, y_min, x_max, y_max, confidence])

            detections = np.array(detections)
            trackers = tracker.update(detections)

            for tracker_data in trackers:
                x1, y1, x2, y2, track_id = tracker_data
                center = ((x1 + x2) / 2, (y1 + y2) / 2)

                if count_region_top < center[1] < count_region_bottom:
                    object_counter += 1

                if track_id not in object_speed:
                    object_speed[track_id] = {"prev_position": center, "speed": 0}

                speed = calculate_speed(object_speed[track_id]["prev_position"], center, fps)
                object_speed[track_id]["speed"] = speed
                object_speed[track_id]["prev_position"] = center

                # Draw bounding box and track ID on frame
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, f'ID: {int(track_id)} | {round(speed, 1)} px/s', (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                csv_writer.writerow([frame_number, int(track_id), int(x1), int(y1), int(x2), int(y2), round(speed, 2)])

            # Write annotated frame to video
            out.write(frame)

    cap.release()
    out.release()
    return output_video_path, output_csv