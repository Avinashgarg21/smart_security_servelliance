from flask import Flask, render_template, Response, request, redirect, url_for, flash
import cv2
import numpy as np
import sqlite3
from keras_facenet import FaceNet
import os
import datetime
import threading
import winsound

app = Flask(__name__)
app.secret_key = 'your_secret_key'
embedder = FaceNet()

# Function to get face embeddings
def get_face_embeddings(image):
    faces = embedder.extract(image, threshold=0.95)
    if faces:
        return faces[0]['embedding']
    return None

# Connect to SQLite database
def connect_db():
    conn = sqlite3.connect('face_database.db')
    return conn

# Function to recognize a face from a new image
def recognize_face(new_embedding):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT name, embedding FROM faces")
    rows = c.fetchall()
    conn.close()

    min_distance = float('inf')
    recognized_name = None
    for row in rows:
        name, embedding = row
        db_embedding = np.frombuffer(embedding, dtype=np.float32)
        distance = np.linalg.norm(new_embedding - db_embedding)
        if distance < min_distance:
            min_distance = distance
            recognized_name = name

    return recognized_name if min_distance < 1.0 else "Unknown"

# Initialize webcam
camera = cv2.VideoCapture(0)

def capture_video():
    while True:
        success, frame = camera.read()
        if not success:
            print("Failed to capture image")
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("Failed to encode image")
            continue

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(capture_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    uploads = os.listdir('static/uploads')
    return render_template('index.html', uploads=uploads)

@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        name = request.form['name']
        images = request.files.getlist('images')
        if not os.path.exists(f'dataset/{name}'):
            os.makedirs(f'dataset/{name}')

        for image in images:
            image_path = os.path.join(f'dataset/{name}', image.filename)
            image.save(image_path)
            embedding = get_face_embeddings(cv2.imread(image_path))
            if embedding is not None:
                insert_face(name, np.array(embedding))

        flash('Person added and model retrained successfully.')
        return redirect(url_for('index'))
    return render_template('add_person.html')

@app.route('/delete_person', methods=['GET', 'POST'])
def delete_person():
    if request.method == 'POST':
        name = request.form['name']
        conn = connect_db()
        c = conn.cursor()
        c.execute("DELETE FROM faces WHERE name = ?", (name,))
        conn.commit()
        conn.close()
        if os.path.exists(f'dataset/{name}'):
            for file in os.listdir(f'dataset/{name}'):
                os.remove(os.path.join(f'dataset/{name}', file))
            os.rmdir(f'dataset/{name}')

        flash('Person deleted successfully.')
        return redirect(url_for('index'))

    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT DISTINCT name FROM faces")
    names = [row[0] for row in c.fetchall()]
    conn.close()
    print(f"Names fetched for deletion: {names}")  # Debug print
    return render_template('delete_person.html', names=names)


# Insert face data into database
def insert_face(name, embedding):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO faces (name, embedding) VALUES (?, ?)", (name, embedding.tobytes()))
    conn.commit()
    conn.close()

def recognize_faces_in_video():
    while True:
        ret, frame = camera.read()
        if not ret:
            break

        # Detect and recognize faces in the frame
        face_embedding = get_face_embeddings(frame)
        if face_embedding is not None:
            recognized_name = recognize_face(face_embedding)
            if recognized_name == "Unknown":
                print("Unknown individual detected")
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"unknown_{timestamp}.jpg"
                filepath = os.path.join('static/uploads', filename)
                cv2.imwrite(filepath, frame)
                print(f"Unknown individual image saved as {filepath}")
                # Play sound using winsound
                winsound.PlaySound('alert.wav', winsound.SND_FILENAME)
            else:
                print(f"Recognized: {recognized_name}")

        # Add a short delay to avoid processing the same frame multiple times
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')

    # Start the face recognition thread
    recognition_thread = threading.Thread(target=recognize_faces_in_video)
    recognition_thread.start()

    app.run(host='0.0.0.0', port=5000, debug=True)
