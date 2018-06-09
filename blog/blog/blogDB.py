# -*- coding: utf-8 -*-

from blog import app
from flask import Flask,g
import sqlite3

#database

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def get_db():
	g.db = connect_db()

@app.teardown_request
def close_db():
	if hasattr(g,'db'):
		g.db.close()