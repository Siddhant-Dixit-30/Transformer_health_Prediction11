from flask import Flask, render_template, request, redirect, url_for, flash
from flask.globals import session
import pickle , re, os
import pandas as pd
from csv import reader
import joblib
import dbConnection as dc

app = Flask(__name__,template_folder='template')
app.secret_key = '1F4453C6EA2C5B454D221285FFFFC'
model_health = joblib.load('D:/Do not touch/BE project/Transformer_health_Prediction11/Model_health.joblib')
model_life = joblib.load('D:/Do not touch/BE project/Transformer_health_Prediction11/Model_life.joblib')

@app.route('/')  
def index():
    if 'username' in session and session['username'] != 'admin':
        return redirect(url_for('user'))
    elif 'username' in session and session['username'] == 'admin':
        return redirect(url_for('admin'))
    else:
        return render_template('login.html')
    
@app.route('/login_nav', methods=['GET','POST'])
def login_nav(): 
    msg='Fill details..'
    return render_template('login.html', msg = msg)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == "admin":
            session['username'] = username
            return redirect(url_for('admin'))
        
        block_status = dc.block(username)
        if block_status == 1:
            flash(f"{username} has been blocked for security reasons. Contact administrator.")
            return redirect(url_for('index'))
        elif block_status == 0:
            login_result = dc.db_login(username, password)
            if login_result == "yes":
                session['username'] = username
                return redirect(url_for('user'))
            else:
                flash('Login Failed. Please check your username and password.')
                return redirect(url_for('index'))
        else:
            flash('An error occurred. Please try again.')
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/user')
def user():
    if 'username' in session and session['username'] != 'admin':
        username=session['username']
        if(dc.block(username)==1):
            msg= username + " has been Blocked for Security Reasons. Contact your Administrator"
            flash(msg)
            session.pop('username', None)
            return redirect(url_for('login_nav'))
        else:
            msg= "Welcome..!! "+ username
            flash(msg)
            return render_template('user_home.html')
    else:
        return redirect(url_for('login_nav'))

@app.route('/admin')
def admin():
    if 'username' in session:
        user = session['username']
        return render_template('admin_home.html')
    else:
        return redirect(url_for('login_nav'))

import pandas as pd
import re

@app.route('/prediction',methods=['GET','POST'])
def prediction():
    if 'username' in session and session['username'] != 'admin':
        username=session['username']
        prediction_type = request.form['prediction-type']
        CO2 = request.form['CO2']
        oxygen = request.form['Oxigen']
        ethylene = request.form['Ethylene']
        hydrogen = request.form['Hydrogen']
        CO = request.form['CO']
        methane = request.form['Methane']
        nitrogen = request.form['Nitrogen']
        if prediction_type == 'health':
             prediction = model_health.predict([[CO2, oxygen,ethylene,
                                          hydrogen, CO, methane,
                                          nitrogen]])[0]
        else:
            prediction = model_life.predict([[CO2,ethylene,
                                          CO,hydrogen, methane,oxygen,
                                          nitrogen]])[0]
        Out=prediction
        print(Out)
        # flash(Out)
        

        return render_template('prediction.html', type=prediction_type,DataOut=prediction) 
    else:
        return redirect(url_for('login_nav'))

@app.route('/usr_status')
def usr_status():
    if 'username' in session and session['username'] == 'admin':
        data = dc.ReadUsers()
        return render_template('user_status.html', data=data)
    else:
        return redirect(url_for('login_nav'))

@app.route('/Activation',methods=['GET','POST'])
def Activation():
    if 'username' in session and session['username'] == 'admin':
        userid = request.form['userid'] 
        out=dc.Activation(userid)
        if out=="yes":
            flash(userid + ' User Activated')
            return redirect(url_for('usr_status'))
        else:
            flash('SomeThing Went Wrong')
            return redirect(url_for('usr_status'))
    else:
        return redirect(url_for('login_nav'))


 
@app.route('/checkagain')
def checkagain():
    return render_template('user_home.html')

@app.route('/scvread')
def scvread():
    myarray=[]
    if 'username' in session:
        filename = 'Overview.csv'
        with open(filename,'r') as read:
            count=0
            csv_reader=reader(read)
            for row in csv_reader:
                count=count+1
                
                myarray.append(row)
                if count>=500:
                    break
            return render_template('csvread.html', DataOut= myarray[1:])
    else:
        return redirect(url_for('login_nav'))

@app.route('/comparative_read')
def comparative_read():
    myarray=[]
    if 'username' in session:
        filename = 'CurrentVoltage.csv'
        with open(filename,'r') as read:
            count=0
            csv_reader=reader(read)
            for row in csv_reader:
                # if row[6] == 'yes':
                count=count+1
                myarray.append(row)
                if count>=500:
                    break
            return render_template('comparative_csv.html', DataOut= myarray[1:])
    else:
        return redirect(url_for('login_nav'))

@app.route('/abusive_read')
def abusive_read():
    myarray=[]
    if 'username' in session:
        filename = 'Overview.csv'
        with open(filename,'r') as read:
            count=0
            csv_reader=reader(read)
            for row in csv_reader:
                count=count+1
                
                myarray.append(row)
                if count>=500:
                    break
            return render_template('csvread.html', DataOut= myarray[1:])
    else:
        return redirect(url_for('login_nav'))



@app.route('/all_analysis')
def all_analysis():
    myarray=[]
    if 'username' in session:
        filename = 'Overview.csv'
        with open(filename,'r') as read:
            count=0
            csv_reader=reader(read)
            for row in csv_reader:
                count=count+1
                myarray.append(row)
                if count>=500:
                    break
            return render_template('all_analysis.html', DataOut= myarray[1:])
    else:
        return redirect(url_for('login_nav'))



@app.route('/usertweetanalysis')
def usertweetanalysis():
    if 'username' in session and session['username'] == 'admin':
        data = dc.ReadTweets()
        return render_template('usertweetanalysis.html', data=data)
    else:
        return redirect(url_for('login_nav'))



@app.route('/register_nav', methods =['GET', 'POST'])
def register_nav():
    return render_template('register.html')


@app.route('/register', methods =['GET', 'POST'])
def register(): 
    msg = '' 
    name = request.form['name'] 
    password = request.form['password'] 
    email = request.form['email']
    mobile = request.form['mobile']
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
        msg = 'Invalid email address !'
        flash(msg)   
    elif not re.match(r'[A-Za-z0-9]+', name): 
        msg = 'Username must contain only characters and numbers !'
        flash(msg)   
    else: 
        dc.db_register(name, email, password, mobile)
        msg = 'You have successfully registered !' 
        flash(msg)   
    return render_template('register.html', msg = msg)  

@app.route('/analysis')
def analysis():
    if 'username' in session and session['username'] == 'admin':
        return render_template('analysis.html')
    else:
        return redirect(url_for('login_nav'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_nav')) 
        
if __name__ == '__main__':  
    app.run(debug=True)
