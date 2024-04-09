from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
import os
import cv2
import numpy as np
import base64
import MySQLdb.cursors
from flask_bcrypt import Bcrypt

app = Flask(__name__, static_folder='static')
app.secret_key = 'abcdefghijkl'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'userdata'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql_conn = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

bcrypt = Bcrypt(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def capture_face(image_data):
    nparr = np.frombuffer(base64.b64decode(image_data.split(',')[1]), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        return None

    (x, y, w, h) = faces[0]
    face_img = img[y:y+h, x:x+w]

    return face_img


# # Function to encode a face image
def encode_face(image):
    # Use a face recognition model or algorithm to encode the face
    # For example, you can use OpenCV's Haar cascades for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = capture_face(gray)
    if len(faces) == 1:
        (x, y, w, h) = faces[0]
        face_roi = gray[y:y+h, x:x+w]
        resized_face_roi = cv2.resize(face_roi, (100, 100))
        return resized_face_roi.flatten()
    return None

# Function to compare two face encodings
def compare_faces(encoding1, encoding2):
    # Implement your own method for comparing face encodings
    # This can be a simple Euclidean distance or a more sophisticated algorithm
    # For simplicity, we'll use a simple Euclidean distance threshold
    if encoding1 is None or encoding2 is None:
        return False
    distance = np.linalg.norm(encoding1 - encoding2)
    return distance < 150  # Increased threshold

def match_image(image_data):
    cursor = mysql_conn.cursor()
    cursor.execute("SELECT name FROM user")
    result = cursor.fetchall()
    for row in result:
        name = row[0]
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], name)
        if not os.path.exists(user_folder):
            continue  # Skip this user if the folder doesn't exist
        user_images = [image for image in os.listdir(user_folder) if os.path.isfile(os.path.join(user_folder, image))]
        for image_name in user_images:
            stored_image = cv2.imread(os.path.join(user_folder, image_name))
            stored_encoding = encode_face(stored_image)
            captured_image = cv2.imdecode(np.frombuffer(base64.b64decode(image_data), np.uint8), cv2.IMREAD_COLOR)
            captured_encoding = encode_face(captured_image)
            match = compare_faces(stored_encoding, captured_encoding)
            if match:
                return True, name
    return False, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql_conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        user = cursor.fetchone()
        if user and password == user['password']:
            session['loggedin'] = True
            session['userid'] = user['id']
            session['name'] = user['name']
            session['email'] = user['email']
            message = 'Logged in successfully!'
        else:
            message = 'Please enter correct email/password!'
    else:
        message = 'Missing email or password field'
    
    return jsonify({'message': message, 'loggedIn': False})



@app.route('/face', methods=['GET', 'POST'])
def face_login():
    if request.method == 'POST':
        if 'loggedin' in session:
            data = request.get_json()
            image_data = data['image'].split(',')[1]
            username = session['name']
            image_name = 'user_image.jpg'
            user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
            os.makedirs(user_folder, exist_ok=True)
            image_path = os.path.join(user_folder, image_name)
            with open(image_path, 'wb') as f:
                f.write(base64.b64decode(image_data))

            is_authenticated, _ = match_image(image_data)
            if is_authenticated:
                return jsonify({'message': f'Welcome, {username}! Image matched.'})
            else:
                return jsonify({'message': 'Login failed. Please try again. Image not matched.'})
        else:
            return jsonify({'message': 'Please login first.'})
    elif request.method == 'GET':
        return render_template('face.html')

if __name__ == '__main__':
    app.run(debug=True)
    
    

# @app.route('/face', methods=['GET','POST'])
# def face_login():
#     if request.method == 'POST':
#         if 'loggedin' in session:
#             data = request.get_json()
#             image_data = data['image'].split(',')[1]
#             username = session['name']
#             image_name = 'user_image.jpg'
#             user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
#             os.makedirs(user_folder, exist_ok=True)
#             image_path = os.path.join(user_folder, image_name)
#             with open(image_path, 'wb') as f:
#                 f.write(base64.b64decode(image_data))

#             is_authenticated, _ = match_image(image_data)
#             if is_authenticated:
#                 return jsonify({'message': f'Welcome, {username}! Image matched.'})
#             else:
#                 return jsonify({'message': 'Login failed. Please try again. Image not matched.'})
#         else:
#             return jsonify({'message': 'Please login first.'})



