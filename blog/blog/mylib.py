# -*- coding: utf-8 -*-

from blogDB import *
import hashlib

class blogInfo(object):
	"""docstring for blogInfo"""
	def __init__(self):
		cursor = g.db.execute('SELECT id,content from info order by id')
		temp = cursor.fetchall()
		self.title = temp[4][1]
		self.subtitle = temp[3][1]
        self.password = temp[2][1]
        self.sidebar = temp[1][1]
        self.tags = temp[0][1]
        self.cate = dict(temp[6:])

    def verify(self,password = ''):
     	m = hashlib.md5()
     	m.update(password)
     	m.update(m.hexdigest()+'123')
     	if m.hexdigest() == self.password:
     		return True
     	else:
     		return False

    def config(self,title='',subtitle='',sidebar='',tags=''):
    	
    	if title:
    		g.db.execute('UPDATE info SET content = ? where id = -1',(title,))
    	if subtitle:
            g.db.execute('UPDATE info SET content = ? where id = -2',(subtitle,))
        if sidebar:
            g.db.execute('UPDATE info SET content = ? where id = -4',(sidebar,))
        if tags:
            g.db.execute('UPDATE info SET content = ? where id = -5',(tags,))

        g.db.commit()

    def setPwd(self,old,new):
    	m = hashlib.md5()
    	m.update(old)
    	m.update(m.hexdigest()+'123')
    	if m.hexdigest() == self.password:
    		m = hashlib.md5()
    		m.update(new)
    		m.update(m.hexdigest()+'123')
    		g.db.execute('UPDATE info SET content = ? where id = -3',(m.hexdigest(),))
    		g.db.commit()
    		return 'Success'
    	else:
    		return 'Couldn\'t match'

    def setCate(self,oldId,newId,content):
    	pass

class Article(object):
	"""docstring for Article"""
	def __init__(self,id=0):
		self.id = id
	def getIt(self):
		cursor = g.db.execute('SELECT title, date, content, tag, abstract, file,img from blog where id = ?',(self.id,))
		arti = cursor.fetchall()[0]
		self.title = arti[0]
		self.date = arti[1]
		if hasattr(self.date,'strftime'):
			self.date = self.date.strftime('%Y-%m-%d %H:%M:%S')
		self.content = arti[2]
        self.tag = arti[3] or ''
        self.abstract = arti[4] #简介
        self.file=arti[5] or '' 
        self.img=arti[6] or ''
	def edit(self,title,tag,img,file,content):
		abstract = abstr(content)
		tags = (tag or '').replace('，',',')
		if self.id:
			g.db.execute('UPDATE blog SET title = ? ,content = ?,abstract = ?,tag = ? ,file = ? ,img=? WHERE ID = ?;', (title, content,abstract,tags,file,img, self.id))
		else:
			g.db.execute('insert into blog (title,tag,file,abstract,content,img) values (?, ?, ?, ?, ?, ?)', (title,tags,file,abstract,content,img))
			cursor = g.db.execute('select id from blog order by id desc limit 1')
			blog = cursor.fetchall()
			self.id = blog[0][0]
		g.db.commit()
		tags = tags.split(',')
        for tag in tags:
            cur.execute('insert into tag (tag, blog) values (?, ?)', (tag, self.id))
        g.db.commit()
	def delIt(self):
		g.db.execute('DELETE FROM blog WHERE id = ? ',(self.id,))
		g.db.execute('DELETE FROM tag WHERE blog = ? ',(self.id,))
        g.db.execute('DELETE FROM comm WHERE blog = ? ',(self.id,))
		g.db.commit()
	def hideIt(self):
		g.db.execute('update blog set file = 0 WHERE id = ? ',(self.id,))
		g.db.execute('DELETE FROM tag WHERE blog = ? ',(self.id,))
        g.db.commit()
	
class Comment(object):
	"""docstring for Comment"""
	def __init__(self, id=0):
		self.id = id
	def getIt(self)：
		cursor = g.db.execute('SELECT content,date,author,id,reply FROM comm WHERE blog = ? ORDER BY id DESC',(self.id,))
		temp = cursor.fetchall()
		#def preRep(c):
		temp.sort(key=lambda s: s[4])
		self.cl = temp
	def getNew(self)：
	def insert():
	def delIt():
	
