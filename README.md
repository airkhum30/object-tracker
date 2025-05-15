# object-tracker
Object Tracker with Flask UI
This project implements real-time object detection and tracking from video files using Flask for the backend and a simple UI. Users can upload a video, and the system will process it, displaying live object detection and tracking results.

**Table of Contents - **
  1. Introduction
  
  2. Features
  
  3. Tech Stack
  
  4. Prerequisites
  
  5. Installation
  
  6. Usage
  
  7. Folder Structure
  
  8. Running with Docker
  
  9. Contributing
  
  10. License
  
  11. Additional Notes

**Introduction**
This project allows users to upload video files for real-time object detection and tracking. The backend is powered by Flask, and the object detection and tracking functionalities are implemented using OpenCV and PyTorch. The UI, created with HTML5, allows easy interaction with the system to upload video files, which are then processed and displayed with live object tracking results.

**Features**
**Real-time Object Detection:** Process and detect objects in uploaded video files.

**Object Tracking:** Track the detected objects across frames in the video.

**File Upload:** Simple interface for uploading video files.

**Results Display:** View the processed video with tracked objects.

**Folder-Based Result Storage:** Save processed videos or results in a results/ directory.

**Docker Support:** Easily containerize and run the application in isolated environments.

**User-Friendly UI:** An intuitive interface that facilitates video upload and real-time feedback.

**Tech Stack**
**The project uses the following technologies:**

**Backend:** Flask (Python Web Framework)

**Frontend:** HTML, CSS, JavaScript (for file upload and video display)

**Object Detection & Tracking:** OpenCV, PyTorch

**Containerization:** Docker (optional for deployment)

**Dependencies:** Listed in **requirements.txt**

**Prerequisites**
To run this project locally or in a Docker container, make sure you have the following:

Python 3.x (Recommended: Python 3.8 or later)

pip (Python's package installer)

Docker (for containerized deployment, optional)

**To check if Python and pip are installed, run:**

bash
Copy
Edit
python --version
pip --version

Installation

**Follow these steps to install and run the project locally:**

**1. Clone the Repository**
Clone the project repository to your local machine:
bash
Copy
Edit
git clone https://github.com/airkhum30/object-tracker.git
cd object-tracker

**2. Set Up a Virtual Environment (Recommended)**
It's recommended to create a virtual environment to manage project dependencies:
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

**3. Install Required Dependencies**
Use pip to install all required dependencies from requirements.txt:

bash
Copy
Edit
pip install -r requirements.txt

**Usage**
**1. Running the Application Locally**
Once the environment is set up, you can start the Flask application:

bash
Copy
Edit
python app.py
By default, the Flask app will run on http://127.0.0.1:5000/. Open this URL in your browser to interact with the UI.

**2. Uploading a Video for Processing**
On the UI's homepage (http://127.0.0.1:5000/):

Use the provided form to upload a video file from your local system.

After uploading, the app will process the video for object detection and tracking.

The processed video will be displayed, showing tracked objects.

**3. Storing Results**
The processed video or results will be saved in the results/ folder. You can view the saved files there.

Folder Structure

object-tracker/
  
  app.py              #Flask app entry point
  
  tracking_util.py    #Object tracking and detection logic
  
  requirements.txt    #Python dependencies
  
Dockerfile            #Docker configuration for deployment

.gitignore            #Git ignore rules

template/             #HTML templates for UI
    index.html        #Main UI page
  
static/               #Static assets (e.g., CSS, JS, images)
  Uploads/            #Input file eg. video.mp4
  
results/              #Folder for storing processed video results



**Running with Docker** 
To run the application in a Docker container, follow these steps:

**Build the Docker image:** docker build -t object-tracker .
:
**Run the Docker container** Docker run -p 5000:5000 object-tracker     #This will start the Flask app inside the Docker container, 

**You can access the app** http://localhost:5000/.

**Contributions** :  Feel free to fork the project and make improvements. If you have suggestions or bug fixes, create a pull request.


**Additional Notes**:  Make sure to have the required dependencies installed, especially PyTorch and OpenCV, for object detection and tracking functionality.

For large video files, the app might take some time to process and track objects, depending on the system's performance.
