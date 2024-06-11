## smart_security_servelliance

The Smart Security Surveillance system is a real-time facial recognition application designed to enhance security by identifying known and unknown individuals using a webcam feed. The system captures video input, processes each frame to detect faces, and matches detected faces against a pre-trained database of known individuals. Unknown faces are logged and an alert is triggered. The system is implemented using Flask for the web interface, OpenCV for video capture and face detection, and FaceNet for generating face embeddings and matching.

## Project Description

The Smart Security Surveillance system is a real-time facial recognition application designed to enhance security by identifying known and unknown individuals using a webcam feed. The system captures video input, processes each frame to detect faces, and matches detected faces against a pre-trained database of known individuals. Unknown faces are logged and an alert is triggered.

## Features

- Real-time video feed from the webcam.
- Face detection and recognition using FaceNet.
- Alert system for unknown individuals.
- Web interface to add and delete known individuals.
- Logs images of unknown individuals for review.

## Use Cases

- Home security systems to monitor entrances.
- Office security to keep track of employees and visitors.
- Automated attendance systems in educational institutions.
- Access control systems in restricted areas.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/smart_security_surveillance.git
   cd smart_security_surveillance


### Install the required dependencies:

  pip install -r requirements.txt

Ensure you have a working webcam connected to your system.

Usage
Run the Flask application:

python app.py

Open your web browser and go to http://127.0.0.1:5000 to access the web interface.

Use the "Add Person" section to register new individuals by uploading their images.

Use the "Delete Person" section to remove individuals from the database.

The live video feed will display real-time recognition results. Unknown individuals will trigger an alert and their images will be saved in the static/uploads directory.

Project Structure
app.py: The main Flask application.
static/uploads: Directory where images of unknown individuals are saved.
templates: HTML templates for the web interface.
requirements.txt: List of Python dependencies.

