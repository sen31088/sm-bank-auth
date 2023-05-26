from flask import request, render_template, url_for, redirect, Blueprint, session
import bcrypt
from models.model_auth import Userlogin, Adminlogin, Userotp
import logging
from utils.sendmail import Sendmail
import random
from dotenv import  load_dotenv
import os

#app = flask.Flask(__name__)

logging.basicConfig(filename='user_activity.log', level=logging.INFO, format='%(asctime)s %(message)s')

auth_ctrl = Blueprint("user_auth", __name__, static_folder='static', template_folder='templates')

load_dotenv()
app_url = os.getenv("URL")
home_url = app_url + '/home'
admin_home_url = app_url + '/admin-home'

def send_otp(userid_in):
    userid = userid_in
    username_found = Userlogin.find_data(userid)
    Acc_Name = username_found['Name']
    email_found = username_found['email']
    otp = str(random.randint(100000, 999999))
    Userotp.delete_data(userid)
    Userotp.save(userid, otp)
    #msg = 'OTP Sent to ' + userid + ' ,Please check your inbox'
    recipient_email = email_found
    username_in = Acc_Name
    subject = '****SM Bank | OTP Verification****'
    message = render_template ('mail-otp.html', username_in = username_in, otp_send= otp)
    Sendmail.send_email(recipient_email, subject, message)
    logging.info(f"OTP sent to {userid}")
    return otp


@auth_ctrl.route('/login', methods=('GET','POST'))
def login():
    msg = ""
    if session.get('otp') is not None:
       # print(" In Route Login session name is true: ", session.get('username'))
        return redirect(home_url)
    else:
        if request.method=='POST':
            #session["name"] = request.form.get("username")
            #print(session["name"])
            #print("In session condition")
            user_found = []
            username_in = request.form['username']
            password_in = request.form['password']
            username_found = Userlogin.find_data(username_in)
            if username_found == 0:
                msg = 'Invalid username ' + username_in
                logging.info(f"{username_in} not found, Invalid username")
                return render_template("index.html", loginmsg = msg)
            else:
                Acc_Name = username_found['Name']
                email_found = username_found['email']
                if username_found:
                    username_val = username_found['userid']
                    passw_check = username_found['password']
                    Activation_status = username_found['Activation_status']
                    if bcrypt.checkpw(password_in.encode('utf-8'), passw_check) and Activation_status == 'Pending':
                        msg = 'Account activation is pending for ' + username_in
                        return render_template('index.html', loginmsg = msg)
                        
                    if bcrypt.checkpw(password_in.encode('utf-8'), passw_check) and Activation_status == 'Suspended':
                        msg = 'Account is Suspended for ' + username_in + '. Please contact Admin.'
                        return render_template('index.html', loginmsg = msg)
                    
                    if bcrypt.checkpw(password_in.encode('utf-8'), passw_check) and Activation_status == 'Activated':
                        a = ''
                        user_found.append(a)
                        #session["username"] = username_val
                        send_otp(username_in)
                        user_found.append(username_found)
                        #otp = str(random.randint(100000, 999999))
                        #Userotp.save(username_in, otp)
                        #session['otp'] = otp
                        session['name'] = username_val
                        #msg = 'OTP Sent to ' + username_in + ' ,Please check your inbox'
                        #recipient_email = email_found
                        #username_in = Acc_Name
                        #subject = '****SM Bank | OTP Verification****'
                        #message = render_template ('mail-otp.html', username_in = username_in, otp_send= otp)
                        #Sendmail.send_email(recipient_email, subject, message)
                        #logging.info(f"OTP sent to {username_val}")
                        return redirect(url_for('user_auth.two_FA_login'))
                    else:
                        msg = 'Wrong password'
                        #print('error: ',msg)
                        logging.info(f"{username_val} failed logged in attempt")
                        return render_template('index.html', loginmsg = msg)
                else:
                    if username_in in session:
                        return redirect(url_for('/'))
                    msg = 'Invalid username ' + username_in
                    logging.info(f"{username_in} not found, Invalid username")
                    return render_template("index.html", loginmsg = msg)    
        return render_template("index.html") 

@auth_ctrl.route('/two-factor-authentication' , methods=('GET','POST'))
def two_FA_login():
        user_session = session.get('name')
        logging.info(f"{user_session} user_session two-factor-authentication in  found")
        logging.info(f"{session} Session data is")
        #user_session_otp = session.get('otp_valid')
        if not user_session :
          return render_template('index.html')
        else:
            userid_in = session['name']
            userlogin_data = Userlogin.find_data(userid_in)
            email_in = userlogin_data['email']
        return render_template('two-factor-index.html', mail_id = email_in)

@auth_ctrl.route('/resend-otp', methods=('GET','POST'))
def resend_otp():
        userid_in = session['name']
        userlogin_data = Userlogin.find_data(userid_in)
        email_in = userlogin_data['email']
        send_otp(userid_in)
        return render_template('two-factor-index.html', mail_id = email_in)


@auth_ctrl.route('/api/v1/verify/two-factor-authentication', methods=('GET','POST'))
def api_verify_two_FA_login():
    if request.method=='POST':
        username_in = session.get('name')
        otp_in = request.form['otp']
        logging.info(f"{username_in} username_in found")
        logging.info(f"{otp_in} otp_in found")
        logging.info(f"{session} Session data is")
        otp_data_found = Userotp.find_otp(username_in)
        logging.info(f"{otp_data_found} OTP data found")
        print("OTP data Found is: ", otp_data_found)
        otp_found = otp_data_found['otp']
        logging.info(f"{otp_found} OTP found")
        print("OTP found is: ",otp_found )
        if otp_in == otp_found:
            Userotp.delete_data(username_in)
            session['otp_valid'] = True
            logging.info(f"{home_url}OTP validated and home url is:")
            print("OTP validated and home url is: ", home_url)
            return redirect(home_url)
        else:
            msg = 'Invalid OTP'
            return render_template('two-factor-index.html', otpmsg = msg)

@auth_ctrl.route('/admin-login', methods=('GET','POST'))
def admin_login():
    msg = ""
    if session.get('username') is not None:
        #print(" In Route Login session name is true: ", session.get('username'))
        return redirect(url_for(admin_home_url))
    else:
        if request.method=='POST':
            session["name"] = request.form.get("username")
            user_found = []
            username_in = request.form['username']
            password_in = request.form['password']
            input_userfound = {'userid': username_in}
            #print("input_userfound" , input_userfound)
            username_found = Adminlogin.find_data(input_userfound)
            if username_found:
                username_val = username_found['userid']
                passw_check = username_found['password']
                #print("Password is: ",passw_check )
                #print("username is: ", username_val)
                if bcrypt.checkpw(password_in.encode('utf-8'), passw_check):
                    a = ''
                    user_found.append(a)
                    session["username"] = username_val
                    user_found.append(username_found)
                    return redirect(url_for(admin_home_url))
                else:
                    msg = 'Wrong password'
                    #print('error: ',msg)
                    return render_template('admin-index.html', loginmsg = msg)
            else:
                if username_in in session:
                    return redirect(url_for('/'))
                msg = 'Invalid username ' + username_in
                return render_template("admin-index.html", loginmsg = msg)    
    return render_template("admin-index.html") 



@auth_ctrl.route("/logout",methods=["POST", "GET"])
def logout():
    user_session = session.get('name')
    session.pop("name", None)
    session.pop("otp_valid", None)
    logging.info(f"{user_session} logged out sucessfully")
    session.clear()
    return redirect("/")