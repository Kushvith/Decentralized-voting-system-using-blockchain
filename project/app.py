# Import necessary libraries
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import logging
import uuid
import base64
import numpy as np
import cv2
from datetime import datetime, date
import json
# Create Flask app
app = Flask(__name__, static_folder='static')


# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'decentralized'

# Initialize MySQL
mysql = MySQL(app)


# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)
logging.exception("mysql: %s", str(mysql))   

# Function to validate PAN card number
def validate_pan_card(pan_number):
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
    if re.match(pattern, pan_number):
        return True
    else:
        return False

# Function to validate password
def validate_password(password):
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    special_chars = "!@#$%^&*()-_+=[]{}|:;<>,.?/~"
    if not any(char in special_chars for char in password):
        return False
    return True

# Function to save uploaded images
def save_uploaded_images(image_data_list, username):
    image_paths = []
    for i, image_data in enumerate(image_data_list):
        nparr = np.frombuffer(base64.b64decode(image_data.split(',')[1]), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if not os.path.exists('uploads/' + username):
            os.makedirs('uploads/' + username)

        filename = str(uuid.uuid4()) + '.jpg'
        filepath = os.path.join('uploads', username, filename)
        cv2.imwrite(filepath, img)
        image_paths.append(filepath)
    return image_paths
@app.route('/test_db',methods=['GET'])
def testdb():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM election')
        account = cursor.fetchone()
        if account:
            message = "account"
        else:
            message = "No data found in the 'election' table."
    except Exception as e:
        message = f'An error occurred while processing your request: {str(e)}'
        logging.exception("Error occurred: %s", str(e))
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

    return json.dumps({"message":message})
# Function to calculate age from date of birth
def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'dob' in request.form and 'pan' in request.form and 'password' in request.form and 'image_data[]' in request.form:
        userName = request.form['name']
        email = request.form['email']
        dob = request.form['dob']
        pan = request.form['pan']
        password = request.form['password']
        image_data_list = request.form.getlist('image_data[]')

        birth_date = datetime.strptime(dob, '%Y-%m-%d').date()
        age = calculate_age(birth_date)
        if age < 18:
            message = 'You must be at least 18 years old to register.'
        elif not validate_pan_card(pan):
            message = 'Invalid PAN card number!'
        elif not validate_password(password):
            message = 'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.'
        else:
            try:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM user WHERE email = %s OR pan = %s', (email, pan))
                account = cursor.fetchone()
                if account:
                    message = 'Account already exists!'
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    message = 'Invalid email address!'
                elif not userName or not email or not dob or not pan or not password:
                    message = 'Please fill out the form!'
                else:
                    image_paths = save_uploaded_images(image_data_list, userName)

                    cursor.execute('INSERT INTO user (name, email, password, dob, pan, age, photo1, photo2, photo3, photo4) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (userName, email, password, dob, pan, age, image_paths[0], image_paths[1], image_paths[2], image_paths[3]))
                    mysql.connection.commit()
                    message = 'You have successfully registered!'
                    return redirect(url_for('login'))

            except Exception as e:
                message = 'An error occurred while processing your request.'
                logging.exception("Error occurred: %s", str(e))
    elif request.method == 'POST':
        message = 'Please fill out the form correctly!'
    return render_template('register.html', message=message)

# Route for home page
# Route for home page
@app.route('/')
def home():
    return render_template('home.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     message = ''
#     if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
#         email = request.form['email']
#         password = request.form['password']
#         try:
#             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password,))
#             user = cursor.fetchone()
#             if user:
#                 session['loggedin'] = True
#                 session['userid'] = user['id']
#                 session['name'] = user['name']
#                 session['email'] = user['email']
#                 message = 'Logged in successfully!'
#                 return render_template('user.html', message=message)
#             else:
#                 message = 'Please enter correct email/password!'
#         except Exception as e:
#             message = 'An error occurred while processing your request.'
#             logging.exception("Error occurred: %s", str(e))
#     return render_template('login.html', message=message)
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password,))
            user = cursor.fetchone()
            if user:
                session['loggedin'] = True
                session['userid'] = user['id']
                session['name'] = user['name']
                session['email'] = user['email']
                message = 'Logged in successfully!'
                return render_template('user.html', message=message, user=user)
            else:
                message = 'Please enter correct email/password!'
        except Exception as e:
            message = 'An error occurred while processing your request.'
            logging.exception("Error occurred: %s", str(e))
    return render_template('login.html', message=message)


# Route for logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)


# # Import necessary libraries
# import os
# from flask import Flask, render_template, request, redirect, url_for, session
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
# import re
# import logging
# import uuid
# import base64
# import numpy as np
# import cv2
# from datetime import datetime, date

# # Create Flask app
# app = Flask(__name__, static_folder='static')
# app.secret_key = 'your_secret_key_here'

# # Configure MySQL
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'userdata'

# # Initialize MySQL
# mysql = MySQL(app)

# # Configure logging
# logging.basicConfig(filename='app.log', level=logging.DEBUG)

# # Function to validate PAN card number
# def validate_pan_card(pan_number):
#     pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
#     if re.match(pattern, pan_number):
#         return True
#     else:
#         return False

# # Function to validate password
# def validate_password(password):
#     if len(password) < 8:
#         return False
#     if not any(char.isupper() for char in password):
#         return False
#     if not any(char.islower() for char in password):
#         return False
#     if not any(char.isdigit() for char in password):
#         return False
#     special_chars = "!@#$%^&*()-_+=[]{}|:;<>,.?/~"
#     if not any(char in special_chars for char in password):
#         return False
#     return True

# # Function to save uploaded images
# def save_uploaded_images(image_data_list, username):
#     image_paths = []
#     for i, image_data in enumerate(image_data_list):
#         nparr = np.frombuffer(base64.b64decode(image_data.split(',')[1]), np.uint8)
#         img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
#         if not os.path.exists('uploads/' + username):
#             os.makedirs('uploads/' + username)

#         filename = str(uuid.uuid4()) + '.jpg'
#         filepath = os.path.join('uploads', username, filename)
#         cv2.imwrite(filepath, img)
#         image_paths.append(filepath)
#     return image_paths

# # Function to calculate age from date of birth
# def calculate_age(birth_date):
#     today = date.today()
#     age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
#     return age

# # Route for user registration
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     message = ''
#     if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'dob' in request.form and 'pan' in request.form and 'password' in request.form and 'image_data[]' in request.form:
#         userName = request.form['name']
#         email = request.form['email']
#         dob = request.form['dob']
#         pan = request.form['pan']
#         password = request.form['password']
#         image_data_list = request.form.getlist('image_data[]')

#         birth_date = datetime.strptime(dob, '%Y-%m-%d').date()
#         age = calculate_age(birth_date)
#         if age < 18:
#             message = 'You must be at least 18 years old to register.'
#         elif not validate_pan_card(pan):
#             message = 'Invalid PAN card number!'
#         elif not validate_password(password):
#             message = 'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.'
#         else:
#             try:
#                 cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#                 cursor.execute('SELECT * FROM user WHERE email = %s OR pan = %s', (email, pan))
#                 account = cursor.fetchone()
#                 if account:
#                     message = 'Account already exists!'
#                 elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#                     message = 'Invalid email address!'
#                 elif not userName or not email or not dob or not pan or not password:
#                     message = 'Please fill out the form!'
#                 else:
#                     image_paths = save_uploaded_images(image_data_list, userName)

#                     cursor.execute('INSERT INTO user (name, email, password, dob, pan, age, photo1, photo2, photo3, photo4) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (userName, email, password, dob, pan, age, image_paths[0], image_paths[1], image_paths[2], image_paths[3]))
#                     mysql.connection.commit()
#                     message = 'You have successfully registered!'
#                     return redirect(url_for('login'))

#             except Exception as e:
#                 message = 'An error occurred while processing your request.'
#                 logging.exception("Error occurred: %s", str(e))
#     elif request.method == 'POST':
#         message = 'Please fill out the form correctly!'
#     return render_template('register.html', message=message)

# # Route for home page
# @app.route('/')
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     message = ''
#     if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
#         email = request.form['email']
#         password = request.form['password']
#         try:
#             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password,))
#             user = cursor.fetchone()
#             if user:
#                 session['loggedin'] = True
#                 session['userid'] = user['id']
#                 session['name'] = user['name']
#                 session['email'] = user['email']
#                 message = 'Logged in successfully!'
#                 return render_template('user.html', message=message, user=user)
#             else:
#                 message = 'Please enter correct email/password!'
#         except Exception as e:
#             message = 'An error occurred while processing your request.'
#             logging.exception("Error occurred: %s", str(e))
#     return render_template('login.html', message=message)


# # Route for logout
# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('userid', None)
#     session.pop('email', None)
#     return redirect(url_for('login'))

# # Run the Flask app
# if __name__ == "__main__":
#     app.run(debug=True)

# Import necessary libraries
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import logging
import uuid
import base64
import numpy as np
import cv2
from datetime import datetime, date

# Create Flask app
app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key_here'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'userdata'

# Initialize MySQL
mysql = MySQL(app)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Initialize face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to validate PAN card number
def validate_pan_card(pan_number):
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
    if re.match(pattern, pan_number):
        return True
    else:
        return False

# Function to validate password
def validate_password(password):
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    special_chars = "!@#$%^&*()-_+=[]{}|:;<>,.?/~"
    if not any(char in special_chars for char in password):
        return False
    return True

# Function to save uploaded images
def save_uploaded_images(image_data_list, username):
    image_paths = []
    for i, image_data in enumerate(image_data_list):
        face_img = capture_face(image_data)
        if face_img is not None:
            if not os.path.exists('uploads/' + username):
                os.makedirs('uploads/' + username)

            filename = str(uuid.uuid4()) + '.jpg'
            filepath = os.path.join('uploads', username, filename)
            cv2.imwrite(filepath, face_img)
            image_paths.append(filepath)
    return image_paths

# Function to calculate age from date of birth
def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# Function to capture face from image data
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

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'dob' in request.form and 'pan' in request.form and 'password' in request.form and 'image_data[]' in request.form:
        userName = request.form['name']
        email = request.form['email']
        dob = request.form['dob']
        pan = request.form['pan']
        password = request.form['password']
        image_data_list = request.form.getlist('image_data[]')

        birth_date = datetime.strptime(dob, '%Y-%m-%d').date()
        age = calculate_age(birth_date)
        if age < 18:
            message = 'You must be at least 18 years old to register.'
        elif not validate_pan_card(pan):
            message = 'Invalid PAN card number!'
        elif not validate_password(password):
            message = 'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.'
        else:
            try:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM user WHERE email = %s OR pan = %s', (email, pan))
                account = cursor.fetchone()
                if account:
                    message = 'Account already exists!'
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    message = 'Invalid email address!'
                elif not userName or not email or not dob or not pan or not password:
                    message = 'Please fill out the form!'
                else:
                    image_paths = save_uploaded_images(image_data_list, userName)

                    cursor.execute('INSERT INTO user (name, email, password, dob, pan, age, photo1, photo2, photo3, photo4) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (userName, email, password, dob, pan, age, image_paths[0], image_paths[1], image_paths[2], image_paths[3]))
                    mysql.connection.commit()
                    message = 'You have successfully registered!'
                    return redirect(url_for('login'))

            except Exception as e:
                message = 'An error occurred while processing your request.'
                logging.exception("Error occurred: %s", str(e))
    elif request.method == 'POST':
        message = 'Please fill out the form correctly!'
    return render_template('register.html', message=message)

# Route for home page
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password,))
            user = cursor.fetchone()
            if user:
                session['loggedin'] = True
                session['userid'] = user['id']
                session['name'] = user['name']
                session['email'] = user['email']
                message = 'Logged in successfully!'
                return render_template('user.html', message=message, user=user)
            else:
                message = 'Please enter correct email/password!'
        except Exception as e:
            message = 'An error occurred while processing your request.'
            logging.exception("Error occurred: %s", str(e))
    return render_template('login.html', message=message)

# Route for logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

