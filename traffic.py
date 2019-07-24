from flask import Flask, render_template, request
import sqlite3 as lite
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/selectrec', methods=['GET'])
def select_record():
    try:
        with lite.connect('traffic.db') as con:
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
    port = os.environ.get('PORT', 5000)
    app.run(debug=True, host='0.0.0.0', port=port)