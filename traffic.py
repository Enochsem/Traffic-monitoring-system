from flask import *
import os
import datetime
from config import credential
import sqlite3 as lite
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY']='8ac7f84d2b39bffc88d30b3616069d'

@app.route('/')
def login():
    return render_template('login.html')

@app.route("/login", methods = ['GET', 'POST'])
@app.route("/index", methods=["GET", "POST"])
def indox():
    print("landing page running...")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # credentials from config files imported
        if username == credential['username'] and password == credential['password']:
            flash('Login successful :)', 'success')
            # flash("You have successfully logged in.", 'success')    # python Toastr uses flash to flash pages
            return render_template('index.html')
        else:
            flash('Login Unsuccessful. Please check username and password', 'error')

    return render_template("index.html")



@app.route('/selectrec', methods=['GET'])
def select_record():
    try:
        with lite.connect('traffic(1).db') as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM data') 
            con.commit()
        
        msg = (datetime.now().strftime('%Y-%m-%d %H:%M:%S')) 
        
        for row in cur: 
           msg = msg + '\n' + str(row[0])  + '\t\t'  + str(row[1]) + '\t\t' +  str(row[2])

    except:
        con.rollback()
        msg = 'error occured'
    finally:
        con.close()
        return msg

@app.route('/addrec', methods=['POST'])
def add_record():
    try:
        image_url = request.form['image_url']
        timestamp = request.form['timestamp']
        speed = request.form['speed']
        camera = request.form['camera']

        with lite.connect('traffic.db') as con:
            cur = con.cursor()
            cur.execute('INSERT INTO data(image, time_stamp, speed, camera_id) VALUES(?, ?, ?, ?)', (image_url, timestamp, speed, camera))

            con.commit()
            msg = (datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ' Record successfully added!'
        
        
    except:
        con.rollback()
        msg = 'error occured'
    finally:
        con.close()
        return msg



if __name__ == '__main__':
    port = os.environ.get('PORT',5000)
    app.run(debug=True, host='0.0.0.0',port=port)