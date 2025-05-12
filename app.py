from flask import Flask, render_template, request, Response, redirect, send_file
import os
import cv2
import threading
from werkzeug.utils import secure_filename
from tracking_utils import process_video
from ultralytics import YOLO
from tracking_utils import process_frame


UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'

app = Flask(__name__)

# Initialize the YOLOv8 model globally
model = YOLO("yolov8n.pt")  # Load the YOLOv8 model (make sure you use the correct model file)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


# Add an /upload route to handle form submission

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "No video part in request", 400
    file = request.files['video']
    if file.filename == '':
        return "No selected file", 400
    filename = secure_filename(file.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(video_path)

    return redirect(f'/stream/{filename}')



# Route: Home page with upload form
@app.route('/')
def index():
    return render_template('index.html')

# Stream video with annotations as frames
@app.route('/stream/<filename>')
def stream_video(filename):
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return Response(generate_video_with_annotations(video_path),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_video_with_annotations(input_path):
    filename = os.path.basename(input_path)
    base_name = os.path.splitext(filename)[0]

    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Save annotated video
    video_out_path = os.path.join(app.config['RESULT_FOLDER'], f'{base_name}_annotated.mp4')
    out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Save CSV
    csv_path = os.path.join(app.config['RESULT_FOLDER'], f'{base_name}_detections.csv')
    csv_file = open(csv_path, 'w')
    csv_file.write('frame_id,class_id,confidence,x1,y1,x2,y2\n')

    frame_id = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        annotated_frame, detections = process_frame(frame)

        # Write frame to video
        out.write(annotated_frame)

        # Write detections to CSV
        for det in detections:
            csv_file.write(f"{frame_id},{','.join(map(str, det))}\n")

        # Stream annotated frame
        _, jpeg = cv2.imencode('.jpg', annotated_frame)
        frame_data = jpeg.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')

        frame_id += 1

    cap.release()
    out.release()
    csv_file.close()




# def generate_video_with_annotations(input_path):
#     filename = os.path.basename(input_path)
#     base_name = os.path.splitext(filename)[0]

#     cap = cv2.VideoCapture(input_path)
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = cap.get(cv2.CAP_PROP_FPS)

#     # Save annotated video
#     video_out_path = os.path.join(app.config['RESULT_FOLDER'], f'{base_name}_annotated.mp4')
#     out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

#     # Save CSV
#     csv_path = os.path.join(app.config['RESULT_FOLDER'], f'{base_name}_detections.csv')
#     csv_file = open(csv_path, 'w')
#     csv_file.write('frame_id,class_id,confidence,x1,y1,x2,y2\n')

#     frame_id = 0
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         annotated_frame, detections = process_frame(frame)

#         # Write frame to video
#         out.write(annotated_frame)

#         # Write detections to CSV
#         for det in detections:
#             csv_file.write(f"{frame_id},{','.join(map(str, det))}\n")

#         # Stream annotated frame
#         _, jpeg = cv2.imencode('.jpg', annotated_frame)
#         frame_data = jpeg.tobytes()
#         yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')

#         frame_id += 1

#     cap.release()
#     out.release()
#     csv_file.close()

if __name__ == '__main__':
    print("🚀 Server running! Visit http://localhost:5000 to upload and process a video.")
    app.run(debug=True, host='0.0.0.0', port=5000)