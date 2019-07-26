from flask import *
import os
import datetime
from config import credential
import sqlite3 
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '5459ed585a54982fc224a8336b094b0a'


@app.route("/", methods = ['GET', 'POST'])
@app.route("/logins", methods=["GET", "POST"])
def logins():
    print("landing page running...")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # credentials from config files imported
        if username == credential['username'] and password == credential['password']:
            flash('Login successful :)', 'success')
            # flash("You have successfully logged in.", 'success')    # python Toastr uses flash to flash pages
            return redirect(url_for('index')) 
        else:
            flash('Login Unsuccessful. Please check username and password', 'error')

    return render_template("login.html")


# you can take this portion out and update it with yours...............................................
def create_table():
    print("Creating table...")
    conn = sqlite3.connect('traff.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS data (image_id int, date1 datetime, speed int, camera_id varchar);")
    conn.commit()

def add_data_to_db(image_id, date1, speed, cameraid):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("insert into data values (?, ?, ?, ?)", (image_id, date1, speed, cameraid))
    conn.commit()
    flash("data inserted SUCCESSFULLY", "success")


@app.route('/index')
def index():
    conn = sqlite3.connect("traff.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("select * from data")
    rows = c.fetchall()
    return render_template("index.html", rows=rows)




@app.route('/add_table')
def add_contact():
    image_id = request.args.get('image_id')
    date1 = request.args.get('date1')
    speed = request.args.get('speed')
    cameraid=request.args.get('cameraid')

    print(image_id)
    print(date1)
    print(speed)
    print(cameraid)
    add_data_to_db(image_id,date1,speed,cameraid)
    return redirect("/", code=302)
# .......................................................................................................

if __name__ == '__main__':
    port = os.environ.get('PORT',5000)
    app.run(debug=True, host='0.0.0.0',port=port)