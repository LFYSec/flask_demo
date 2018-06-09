# -*- coding:utf-8 -*- q

from flask import Flask,render_template
from sqlalchemy import func
from main import app
from models import db,User,Post,Tag,Comment,posts_tags

def sidebar_data():
	""" Set sidebar func """

	recent = db.session.query(Post).order_by(
			Post.publish_date.desc()
		).limit(5).all()

	top_tags = db.session.query(
			Tag,func.count(posts_tags.c.post_id).label('total')
		).join(
			posts_tags
		).group_by(Tag).order_by('total DESC').limit(5).all()
	return recent,top_tags

@app.route('/')
@app.route('/<int:page>')
def home(page=1):
	"""View func for home"""

	posts = Post.query.order_by(
			Post.publish_date.desc()
		).paginate(page,10)

	recent,top_tags = sidebar_data()

	return render_template('home.html',
							posts = posts,
							recent = recent
							top_tags = top_tags)

@app.route('/post/<string:post_id>')
def post(post_id):
	"""View function for post page"""

	post = Post.query(Post).get_or_404(post_id)
	