from distutils.command.config import config
from unicodedata import name
from pkg_resources import to_filename
import pyrebase

config = {
    "apiKey": "AIzaSyAQKLnnL3KBMmkG1m1hyiwbIUulLVwCzpE",
    "authDomain": "my-eng-eca4e.firebaseapp.com",
    "databaseURL": "https://my-eng-eca4e-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "my-eng-eca4e",
    "storageBucket": "my-eng-eca4e.appspot.com",
    "messagingSenderId": "142903269026",
    "appId": "1:142903269026:web:cf5490ec4709685f3ba9fb",
    "measurementId": "G-NBBJTPEWHN"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

from flask import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def basic():
	if request.method == 'POST':
		if request.form['submit'] == 'add':

			name = request.form['name']
			db.child("todo").push(name)
			todo = db.child("todo").get()
			to = todo.val()
			return render_template('index.html', t=to.values())
		elif request.form['submit'] == 'delete':
			db.child("todo").remove()
		return render_template('index.html')
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)
