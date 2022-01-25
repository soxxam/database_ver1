from asyncio.windows_events import NULL
import datetime
from pydoc import Doc
import random
from unicodedata import category
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import *
from collections import OrderedDict
from flask.json import JSONEncoder
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'

cred = credentials.Certificate("keyfirebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# db.collection('persons').add({'name':'John', 'age':40})

@app.route('/form', methods=['GET', 'POST'])
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

			# quesId = db.collection(u'QaA_Category').document(u'Id_category')
			# quiz_id_detail =
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
	return render_template('form.html')


@app.route('/test', methods=['GET', 'POST'])
def test():
	return render_template('test.html')

@app.route('/doquiz', methods=['GET', 'POST'])
def doquiz():
	return render_template('doquiz.html')

@app.route('/createquiz', methods=['GET', 'POST'])
def createquiz():
	if request.method == 'POST':
		if request.form['submit'] == 'addquiz':
			slug = request.form['slug']
			title = request.form['title']

			Q = db.collection('Quiz').add({ 'Slug': slug, 'Title': title})
			QuizId = Q[1].id
			ques_pas = db.collection(u'Question').where('id_Category', '==', "n6fIj5OpPkJ17wUgYA2o").stream()
			ques_nps = db.collection(u'Question').where('id_Category', '==', "BqDs7eNcSXlHb8d9uTCh").stream()
			a = []
			for ques_pa in ques_pas:
				a.append(ques_pa.id)

			for i in range(5):
				ques_a = random.choice(a)
				Q_detail_a = db.collection('Quiz_Detail').add({'Id_Quiz': QuizId, 'Id_Ques': ques_a})

			b = []
			for ques_np in ques_nps:
				b.append(ques_np.id)
				print(f'{ques_np.id}')
			#
			for i in range(5):
				ques_b = random.choice(b)
				Q_detail_b = db.collection('Quiz_Detail').add({'Id_Quiz': QuizId, 'Id_Ques': ques_b})

	return render_template('createquiz.html')

@app.route('/', methods=['GET', 'POST'])
def index():


	return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
	users_ref = db.collection(u'Question').stream()
	docs_id = []
	title =[]
	for doc in users_ref:
		docs_id.append(doc.to_dict())
		print(f'{doc.id} => {doc.to_dict()}')
	for i in docs_id:
		print(i['title'])
		print("\n")
		title.append(i['title'])
	return render_template('quiz.html', docs_id=docs_id,title=title)

@app.route('/api/quiz', methods=['GET', 'POST'])
def api_quiz():
	users_ref = db.collection(u'Question').stream()
	data = OrderedDict([(doc.id, doc.to_dict()) for doc in users_ref])
	
	return jsonify(data)



	return jsonify(data)

if __name__ == '__main__':
	app.run(debug=True)