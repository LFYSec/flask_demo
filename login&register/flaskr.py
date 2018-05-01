from flask import Flask
from flask import render_template,request,session,url_for,redirect,flash,g
import sqlite3
import config
from contextlib import closing

app = Flask(__name__)
app.config.from_object('config') #if there isn't import config,this sentence isn't needed
#app.config.from_envvar()

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])
'''
def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('init.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()
'''

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	if hasattr(g,'db'):
		g.db.close()

@app.route('/')
def index():
	if session.get('user') is None:
		return redirect(url_for('login'))
	else:
		return render_template('hello.html',name=session['user'])

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		name = request.form['user']
		passwd = request.form['passwd']
		cursor = g.db.execute('select * from users where username=? and passwd=?',[name,passwd])
		if cursor.fetchall() is not None:
			session['user'] = name
			flash('login success!')
			return redirect(url_for('index'))
		else:
			flash('no such user','error')
			return redirect(url_for('login'))
	else:
		return render_template('login.html')

@app.route('/logout')
def logout():
	session['user'] = None
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run()