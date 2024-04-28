import base64
import datetime
import hashlib
import json
import logging
import os
import re
import uuid
import cv2
from flask_mysqldb import MySQL
import MySQLdb.cursors
import numpy as np
from database.database import PeersDb
import requests
from flask import jsonify, render_template, redirect, request,session,url_for
from flask import flash
import urllib.parse
from app import app
from datetime import date
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib
from flask_cors import CORS
# The node with which our application interacts, there can be multiple
# such nodes as well.
app.config['MYSQL_HOST'] = '192.168.1.101'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'decentralized'
app.secret_key = "this_my_secreat_key_cant_be_cracked_by_anyone"
# Initialize MySQL
mysql = MySQL(app)
app.config['DEBUG'] = True
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)
# Use the default Haar cascade XML file for face detection
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

vote_check=[]

posts = []


    
def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    peerdb = PeersDb()
    parsed_url = urllib.parse.urlparse(request.host_url)

    new_port = 8000

    parsed_url = parsed_url._replace(netloc=parsed_url.netloc.replace(':5000', ':' + str(new_port)),scheme='http')

    new_url = urllib.parse.urlunparse(parsed_url)

    print(new_url)
    if new_url not in peerdb.read():
        peerdb.write([new_url])
    current_len = 0
    for node in peerdb.read():
        try:
            print(node)
            response = requests.get('{}/chain'.format(node), timeout=3)
            print(f"{node} {response.content}")
            length = response.json().get('len', 0)
            chain = response.json().get('chain', [])
            
            if length > current_len:
                current_len = length
                longest_chain = chain
                
            if longest_chain:
                content = []
                vote_count = []
                chain = response.json().get('chain', [])
                
                for block in chain:
                    for tx in block.get("transactions", []):
                        tx["index"] = block.get("index")
                        tx["hash"] = block.get("previous_hash")
                        content.append(tx)
                        
                        if block.get('index', 0) != 0:
                            if tx.get('voter_id') not in vote_check:
                                print("vote_check", vote_check)
                                vote_check.append(tx.get('voter_id'))
                
                global posts
                posts = sorted(content, key=lambda k: k.get('timestamp', 0), reverse=True)
    
        except requests.exceptions.RequestException:
            # If the node is not reachable, remove it from the peers database
            print("last nodes",node)
            peerdb.remove_node(node)
            

def validate_pan_card(pan_number):
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
    if re.match(pattern, pan_number):
        return True
    else:
        return False       
@app.route('/test_db',methods=['GET'])
def testdb():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM election')
        account = cursor.fetchone() 
        if account:
            message = account['name']
        else:
            message= "error in fetching db"
    except Exception as e:
            message = f'An error occurred while processing your request.'
            logging.exception("Error occurred: %s", str(e))   
    return json.dumps({"message":message})

def extract_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    print(len(faces))
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        face = frame[y:y+h, x:x+w]
        return face
    else:
        return None

def extract_faces(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_points = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
        
        return face_points
    except Exception as e:
        print(f"Error in extract_faces: {e}")
        return img

def crop_faces(img, face_points):
    cropped_faces = []
    for (x, y, w, h) in face_points:
        face = img[y:y+h, x:x+w]
        cropped_faces.append(face)
    return cropped_faces
def train_model():
    faces = []
    labels = []
    userlist = os.listdir('uploads/')
    for user in userlist:
        for imgname in os.listdir(f'uploads/{user}'):
            img = cv2.imread(f'uploads/{user}/{imgname}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)
    faces = np.array(faces)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces, labels)
    joblib.dump(knn, 'static/face_recognition_model.pkl')
    print("training completed")
    
def identify_face(facearray):
    model = joblib.load('static/face_recognition_model.pkl')
    return model.predict(facearray)

def save_uploaded_images(image_data_list, username):
    image_paths = []
    for i, image_data in enumerate(image_data_list):
        nparr = np.frombuffer(base64.b64decode(image_data.split(',')[1]), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        detected_faces = extract_faces(img)
        if len(detected_faces) == 0:
            print(f"No faces found in image {i}")
            continue  # Skip saving if no faces found in this image

        cropped_faces = crop_faces(img, detected_faces)
        if not os.path.exists('uploads/' + username):
            os.makedirs('uploads/' + username)

        for face_index, face_img in enumerate(cropped_faces):
            filename = f"{username}_{i}_{face_index}.jpg"
            filepath = os.path.join('uploads', username, filename)
            cv2.imwrite(filepath, face_img)
            image_paths.append(filepath)
    return image_paths
@app.route('/logout')
def logout():
    session.clear()  
    return redirect(url_for('login'))
@app.route('/login',methods=['GET','POST'])
def login():
    message = ""
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        image_data_list = request.form['image_data[]']
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM voters WHERE email = %s AND password = %s AND status = 1', (email, password))
            account = cursor.fetchone()
            if account:
                train_model()
                print("accouny login")
                nparr = np.frombuffer(base64.b64decode(image_data_list.split(',')[1]), np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                detected_face = extract_face(img)
                
                if detected_face is not None:
                    print("face detected")
                    (x, y, w, h) = extract_faces(img)[0]
                    face = cv2.resize(img[y:y+h, x:x+w], (50, 50))
                    identified_person = identify_face(face.reshape(1, -1))[0]
                    print(identified_person)
                    if identified_person == email:
                        print("signed up successfull")        
                        session['email']= email
                        print(str(account))
                        session['minmat'] = account[8]
                        return redirect(url_for('home'))
                    else:
                        print("face not matched")
                        message="face not matched try coming to light"
                else:
                    print("face not found")
                    message = "Face not found in the image"
            else:
                message = 'Email and password are incorrect'
        except Exception as e:
            message = f'An error occurred while processing your request.'
            logging.exception("Error occurred: %s", str(e))        
    return render_template("login.html",message=message) 
def today_parties(is_vote=False):
    party = []
    cursor = mysql.connection.cursor()
    today_date = date.today()
    query = f"""
    SELECT * FROM election 
    WHERE time_election = %s {'AND status = "pending"' if is_vote else ''}
    """
    cursor.execute(query, (today_date,))
    election = cursor.fetchone()
    if election:
        election_id = str(election[0])
        cursor.execute("SELECT * FROM `election_party` INNER JOIN election ON election.id = election_party.election_id INNER JOIN party ON party.id = election_party.party_id WHERE election_party.election_id = %s",(election_id))
        party_data = cursor.fetchall()
        for party_row in party_data:
            print(str(party_row))
            party_dict = {
                "election_id":party_row[0],
                "election_name":party_row[3],
                "status":party_row[6],
                "party_id":party_row[7],
                "party_name":party_row[8],
                "candidate_name":party_row[9],
                "age":party_row[10],
                "image":party_row[11]
            }
            party.append(party_dict)
    return party
@app.route('/contact',methods=['POST'])
def contact():
    name = request.form['username']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO `contact` ( `name`, `email`, `phone`, `message`) VALUES (%s, %s, %s, %s)',(name,email,phone,message))
    mysql.connection.commit()
    return render_template("index.html",message=1)
   
@app.route('/fetch_results',methods=['GET'])
def fetchResults():
    cursor = mysql.connection.cursor()
    vote_gain = []
    fetch_posts()
    for post in posts:
        vote_gain.append(post["party"])
    party = today_parties()
    print(party)

    party_name_counts = {party_item["party_name"]: 0 for party_item in party}

    for party_name in vote_gain:
        if party_name in party_name_counts:
            party_name_counts[party_name] += 1
        else:
            party_name_counts[party_name] = 1
    cursor.execute("UPDATE `election` SET `status`='completed' WHERE id = %s",(party[0]['election_id'],))
    mysql.connection.commit()
    for name,res in party_name_counts.items():
        cursor.execute('INSERT INTO `results`(`party_name`, `election`, `result`) VALUES (%s,%s,%s)',(name,party[0]['election_id'],res))
        mysql.connection.commit()
    cursor.close()
    peer = PeersDb()
    for p in peer.read():
        response = requests.get('{}/clean_data'.format(p), timeout=3)
        if response.status_code == 200:
            continue
    data = {"message": "Success"}
    callback = request.args.get('callback')
    if callback:
        jsonp_response = f"{callback}({jsonify(data).data.decode('utf-8')})"
        return jsonp_response, 200, {'Content-Type': 'application/javascript'}
    else:
        return jsonify(data), 200
    
@app.route('/home',methods=['GET','POST'])
def home():
    message = ""
    electionMSg = []
    fetch_posts()
    print("fetching the post........")
    vote_gain = []
    party = []
    print(session.get("email"))
    if not session.get("email"):
        return redirect(url_for("signup"))
    for post in posts:
        vote_gain.append(post["party"])
    party = today_parties(is_vote=True)
    if not party:
        message = "No Election Today Checkout the Announcement"
    print(vote_check)
    return render_template("home.html",message=message,electionMSg=party)
    
@app.route('/signup',methods=['GET','POST'])
def signup():
    message = ""
    if request.method == "POST":
        firstname = request.form['first_name']
        lastname = request.form['last_name']
        email = request.form['email']
        phno = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        pan = request.form['pan_no']
        age = request.form['age']
        dob = request.form['dob']
        gender = request.form['gender']
        image_data_list = request.form.getlist('image_data[]')
        minmat_add = hashlib.sha256(email.encode()).hexdigest()
        if password != confirm_password:
            message = "password should match"
        elif int(age) < 18:
            message = "age should be equal or greater than 18"
        # elif not validate_pan_card(pan):
        #     message = "enter the valid pan number"
        else:
          try:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM voters WHERE email = %s OR pan = %s', (email, pan))
            account = cursor.fetchone()
            if account:
                message = 'Account already exists!'
            else:
                image_paths = save_uploaded_images(image_data_list, email)
                print(len(image_paths))
                if(len(image_paths) > 1):
                    cursor.execute('INSERT INTO `voters` (`first_name`, `last_name`, `email`, `phone`, `password`, `pan`, `dob`,`minmat_add`,`status`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(firstname,lastname,email,phno,password,pan,dob,minmat_add,0))
                    mysql.connection.commit()
                    message = 'You have successfully registered! and please wait for verification'
                else:
                    message = "Make sure your face is visible properly"
          except Exception as e:
                message = f'An error occurred while processing your request.'
                logging.exception("Error occurred: %s", str(e))
    return render_template("signup.html",message=message)

@app.route('/')  
def index():
    return render_template('index.html')
def format_date(date):
    dt_object = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    formatted_date = dt_object.strftime("%b %d %Y")
    return formatted_date
@app.route('/announcement')
def announce():
    annouce = []
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM announcement')
    account = cursor.fetchall()
    for row in account:
        print(row)
        row_item = {
            "date": format_date(str(row[2])),
            "message":row[1]
        }
        annouce.append(row_item)
    return render_template('announcement.html',annouce=annouce)
@app.route('/results')
def results():
    message = ""
    vote_gain = []
    fetch_posts()
    for post in posts:
        vote_gain.append(post["party"])
    party = today_parties()
    if not party:
        message = "Today No Elections Sheduled"
    return render_template("results.html",message=message,political_parties=party,vote_gain=vote_gain)
@app.route('/submit', methods=['POST'])
def submit_textarea():
    VOTER_ID = []
    """
    Endpoint to create a new transaction via our application.
    """
    message = ""
    party = request.form["party"]
    voter_id = request.form["voter_id"]
    post_object = {
        'voter_id': voter_id,
        'party': party,
    }
    peerdb = PeersDb()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM voters')
    account = cursor.fetchall()
    for row in account:
        VOTER_ID.append(row[8])
    if voter_id not in VOTER_ID:
        message = 'Voter ID invalid, please select voter ID from sample!'
        return render_template('home.html',message=message)
    if voter_id in vote_check:
        message = 'Voter ID ('+voter_id+') already vote, Vote can be done by unique vote ID only once!'
        return render_template('home.html',message=message)
    else:
        for node in peerdb.read():
            new_tx_address = "{}/new_transaction".format(node)
            requests.post(new_tx_address,
                    json=post_object,
                    headers={'Content-type': 'application/json'})
            vote_check.append(voter_id)
            message = 'Voted to '+party+' successfully!'
        return render_template('home.html',message=message)


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M')
 