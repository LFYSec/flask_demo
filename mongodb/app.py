from flask import Flask,request,abort,url_for,render_template,redirect
from time import time
from bson.objectid import ObjectId
from bson.json_util import dumps
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient()

DATABASE = 'todos'
db = client[DATABASE]

COLLECTION = 'todos'	
col = db[COLLECTION]

class Todo(object):
	@classmethod
	def create_doc(cls,content):
		return {
			'content':content,
			'created_at':time(),
			'is_finished':False,
			'finished_at':None
		}

@app.route('/todo/',methods=['GET'])
def index():
	todos = col.find({})
	return render_template('index.html',todos=todos)

@app.route('/todo/',methods=['POST'])
def  add():
	content = request.form.get('content',None)
	if not content:
		abort(400)
	col.insert(Todo.create_doc(content))
	return redirect(url_for('index'))

@app.route('/todo/<content>/finished')
def finish(content):
	result = col.update_one(
		{'content':content},
		{
			'$set':{
				'is_finished':True,
				'finished_at':time()
			}
		}
	)
	return redirect(url_for('index'))

@app.route('/todo/<content>')
def delete(content):
	result = db.todos.delete_one(
		{'content':content}
	)
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=True)
