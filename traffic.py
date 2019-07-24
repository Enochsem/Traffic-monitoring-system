from flask import *
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('tryhow_css_login_form_modal.html')

@app.route('/data')
def data():
    return render_template('data.html')


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(debug=True, host='0.0.0.0',port=port)