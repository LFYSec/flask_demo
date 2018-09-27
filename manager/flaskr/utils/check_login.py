from flask import url_for,redirect,session
from functools import wraps

def is_login(func):
	'''
	a wraps used to chech_login
	'''
	@wraps(func)
	def check_login(*args,**kwargs):
		user_id = session.get('user_id')
		if user_id:
			return func(*args,**kwargs)
		else:
			return redirect(url_for('user.login'))
	return check_login