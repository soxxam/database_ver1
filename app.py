from asyncio.windows_events import NULL
import datetime
from unicodedata import category
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import *
app = Flask(__name__)

cred = credentials.Certificate("keyfirebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# db.collection('persons').add({'name':'John', 'age':40})

@app.route('/', methods=['GET', 'POST'])
def basic():
	if request.method == 'POST':
		if request.form['submit'] == 'add':
			category = request.form['category']
			question = request.form['question']
			answer1 = request.form['answer1']
			answer2 = request.form['answer2']
			answer3 = request.form['answer3']
			answer4 = request.form['answer4']
			title = request.form['title']
			# down here is get true answer
			if(title == ""):
				return 'Nhập cái title vào người ơi'
			try:
				flexRadioDefault = request.form['flexRadioDefault']
				true_ans = request.form[flexRadioDefault]
			except:
				return 'Chọn cái đáp án đúng đi người ơi'
			# end
			# down here is get id_category from name_category
			id_category = db.collection('QaA_Category').where('name', '==', category).stream()
			id_cate = ""
			for doc in id_category:
				id_cate = doc.id
			# end get id
			# down here is add question to database on firebase firestore
			d = db.collection('Question').add({'name_Question':question, 'id_Category':id_cate ,'title':title})
			docId = d[1].id
			print('Id:',docId)
			# ans = db.collection('Option').add({'id_Question':docId, 'True_ans':true_ans})
			new_city_ref = db.collection("Option").document()
			new_city_ref.set(
				{
					u'id_Question': docId,
					u'Option_ans': [answer1, answer2, answer3, answer4],
					u'True_ans': true_ans,
					u'date':  datetime.datetime.now(tz=datetime.timezone.utc),
				}
			)
			return render_template('index.html')
	return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
	return render_template('test.html')

if __name__ == '__main__':
	app.run(debug=True)