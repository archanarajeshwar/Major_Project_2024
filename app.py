from datetime import datetime
from flask import Flask, render_template,request,json,redirect,jsonify,flash
import mysql.connector                          
from collections.abc import Mapping
import pymysql
from flask   import session
import cv2 
import base64
from io import BytesIO
import numpy as np
import math
import pandas as pd
from base64 import b64encode
from datetime import datetime
import os 
from PIL import Image 
from flask_mail import Mail 
from werkzeug.utils import secure_filename
import subprocess
from pathlib import Path
from maksad_khatam1 import detect_anemia
from flask_cors import CORS
from address import gmaps
import requests
from geopy.geocoders import Nominatim
from text_processor import TextProcessor
from data_extraction import ExtractPDFData
from prompt import Prompt
 



app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("Set the FLASK_SECRET_KEY environment variable before starting the application.")
CORS(app)

#db connection
conn = pymysql.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ.get("DB_USER", "root"),
    password=os.environ["DB_PASSWORD"],
    database=os.environ.get("DB_NAME", "anemia_detection"),
)
cursor=conn.cursor()

hb_threshold={
    'male':13,
    'female':12,
    'pregnant':10,
    'children':10

}



@app.route("/")
def main():
    return render_template('index.html')
  

@app.route('/signup')
def Showsignup():
    return render_template('signup.html')

@app.route('/api/signup',methods=['POST'])
def signUp():
    try:
        username = request.form['inputName']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        
        selectquery = "select * from user where username ='%s' "%username
        cursor=conn.cursor()
        cursor.execute(selectquery)
        data = cursor.fetchall()
        if len(data)== 0:
            conn.commit()
            insertquery = "INSERT INTO user (id, username, password, email) VALUES (null, %s, %s, %s)"
            values = (username, password, email)
            cursor.execute(insertquery, values)
            conn.commit()
            cursor.close() 
            return render_template('signup.html')
            
        else:
            return json.dumps({'error': str(data[0])})
    except Exception as e:
        return json.dumps({'error':str(e)})  

        
@app.route('/signin')
def showSignin():
    return render_template('signin.html')


@app.route('/api/validateLogin',methods=['POST'])
def validateLogin():
    try:
        email = request.form['inputEmail']
        password = request.form['inputPassword']
 
     # connect to mysql
        print("before proce")
        cursor=conn.cursor()
        cursor.execute("select * from user where email ='%s' and password='%s'"%(email,password))
        print('after proc')
        data = cursor.fetchall()
        conn.commit()
        print(data)
        if len(data) > 0:
            session['userid'] = data[0][0]
            print('inside if')
            return  render_template('userhome.html',user=data)
            
        else:
            return render_template('error.html',error = 'Wrong Email address or Password')
 
    except Exception as e:
        return render_template('error.html',error = str(e))

@app.route('/userHome')     
def userHome():
    if session.get('userid'):
        cursor = conn.cursor()
        username =str(session.get('user_id'))
        selectquery="select username from user where username='%s'"%(username)
        print(selectquery)  
        cursor.execute(selectquery) 
        data= cursor.fetchall() 
        print(data)     
        cursor.close()  
        return render_template('userhome.html',username=data)
    else:
        return render_template('error.html',error = 'Unauthorized Access')


@app.route('/profile')
def profile():  
    if session.get('userid'):
        cursor = conn.cursor()
        userid = int(session.get('userid'))
        selectquery = "SELECT * FROM user WHERE id=%s"
        cursor.execute(selectquery, (userid,))
        data = cursor.fetchall()
        cursor.close()
        return render_template('userprofile.html', userprofile=data)
    else:
        return render_template('error.html', error='Unauthorized Access')
    

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')


def get_latest_exp_folder():
    exp_folders = sorted(Path('yolov5/runs/detect/').glob('exp*'), key=os.path.getmtime, reverse=True)
    if exp_folders:
        latest_exp_folder = exp_folders[0]
        latest_image = next(latest_exp_folder.glob('*.jpg'), None)
        if latest_image:
            return jsonify({"latest_image": str(latest_image.relative_to('yolov5/runs/detect/'))})
    return jsonify({"error": "No experiment folders found"})

# Define the upload folder
UPLOAD_FOLDER = 'input_img'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)      

# Configure upload folder in app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/detect')
def detect():
    return render_template('detect.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file'] 
    person=request.form['options']
    if file:
        filename = "input_img.jpg"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    data = detect_anemia()
    thres = hb_threshold[person]
    if(data<thres):
        result="Result : Anemia is detected."
    else:
        result="Result : Anemia is Not detected."
    print(person,hb_threshold[person]) 
    return  jsonify({'data': data,'result':result})
    


@app.route('/hospitals', methods=['POST'])
def hospitals():
    latitude = request.get_json()['latitude'] 
    longitude = request.get_json()['longitude'] 
    print(latitude,longitude)
    lat = 19.0443
    long = 72.8204
    # hospital_data = gmaps(latitude,longitude)
    hospital_data = gmaps(lat,long)
    return jsonify(hospital_data)

@app.route('/hosp', methods=['GET'])
def hosp():
    return render_template('hospital.html')

@app.route("/cbc", methods=["GET", "POST"])
def upload_pdf():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file:
            filename = file.filename
            file.save(os.path.join("uploads/pdf", filename))
            file_path = os.path.join("uploads/pdf", filename)
            weight = float(request.form['weight'])
            height = float(request.form['height'])
            age = float(request.form['age'])
            activity_level = float(request.form['activity'])
            disease = request.form['disease']
            gender = request.form['gender']

            if gender == "Male" :
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161

            daily_calories = bmr * activity_level
            
            graphLab = ['Neutrophils', 'Lymphocytes', 'Eosinophils', 'Monocytes', 'Basophils']
            extract_pdf = ExtractPDFData()
            extracted_data = extract_pdf.extract_information(file_path)[0]
            graphVal = [extract_pdf.extract_value(extracted_data, keyword) for keyword in graphLab]
            print(graphVal)
            
            summary, type_of_amemia, diet, daily_activity , prevention = Prompt().generate_prompt(extracted_data,bmr , daily_calories , activity_level,disease)
            breakfast, lunch, dinner = TextProcessor().processor(diet)
            activities = TextProcessor().extract_activities(daily_activity)
            
            dietVal = {
                    'breakfast': breakfast,
                    'lunch': lunch,
                    'dinner': dinner,
                }
            
            data = {
                'summary': summary, 
                'type_of_amemia': type_of_amemia, 
                'daily_activity': activities,
                'graphLab':graphLab,
                'graphVal': graphVal,
                'diet': dietVal,
                'weight': weight,
                'height': height,
                'activity_level': activity_level,
                'disease' : disease,
                'prevention' : prevention,
                'bmr' : bmr
            }

            graphData = {
                'graphLab':graphLab,
                'graphVal': graphVal,
            }
            
            return render_template("home.html", data=data , graphData=graphData)
    else:
        return render_template("upload.html")

if __name__ =='__main__':
    app.run(debug=True, port=5000)    