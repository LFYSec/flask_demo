from flask import Blueprint,redirect,url_for,session,render_template,request

from App.models import db,User,Grade,Student,Permission,Role
from utils.check_login import is_login


user_blueprint = Blueprint('user',__name__)


@user_blueprint.route('/create_db/')
def create_db():
	db.create_all()


@user_blueprint.route('/drop_db/')
def drop_db():
	db.drop_all()
	return 'Drop successful!'


@user_blueprint.route('/home/',methods=['GET'])
@is_login
def home():
	if request.method == 'GET':
		return render_template('index.html')


@user_blueprint.route('/head/',methods=['GET'])
@is_login
def head():
	if request.method == 'GET':
		user = session.get('username')
		return render_template('head.html',user=user)


@user_blueprint.route('/left/', methods=['GET'])
def left():
    """左侧栏"""
    if request.method == 'GET':
        # 获取登录的用户信息
        user = session.get('username')
        # 获取用户的权限
        permissions = User.query.filter_by(username=user).first().role.permission
        return render_template('left.html', permissions=permissions)


@user_blueprint.route('/register/',methods=['GET','POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')

	if request.method == 'POST':
		username = request.form.get('username')
		pwd1 = request.form.get('pwd1')
		pwd2 = request.form.get('pwd2')

		# the flag of check
		flag = True

		if username == '' or pwd1 == '' or pwd2 == '':
			msg,flag = 'Sth is empty!',False

		if len(username) > 16:
			msg,flag = 'Username is too long',False

		if pwd1 != pwd2:
			msg,flag = 'Passwd is different',False

		if not flag:
			return render_template('register.html',msg=msg)

		u = User.query.filter_by(username=username).first()

		if u:
			msg = 'Username has been registered!'
			return render_template('register.html',msg=msg)

		uesr = User(username=username,password=pwd1)
		user.save()

		return redirect(url_for('user.login'))


@user_blueprint.route('/login/',methods=['GET','POST'])
def login():
	'''
	login
	'''
	if request.method == 'GET':
		return render_template('login.html')

	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		#test filtered
		if all([username,password]):
			msg = 'Not completely'
			return render_template('login.html',msg=msg)
		#check
		user = User.query.filter_by(username=username,password=password).first()

		if user:
			#write session
			session['user_id'] = user.u_id
			session['username'] = user.username
			return render_template('index.html')
		else:
			msg = 'Passwd error'
			return render_template('login.html',msg=msg)



@user_blueprint.route('/logout/',methods=['GET'])
def logout():
	"""
	logout
	"""
	if request.method == 'GET':
		session.clear()
		return redirect(url_for('user.login'))


@user_blueprint.route('/grade/',methods=['GET','POST'])
@is_login
def grade_list():
	'''
	the list of classes
	'''
	if request.method == 'GET':
		#the page which you query
		page = int(request.args.get('page',1))
		#page_num
		page_num = int(request.args.get('page_num',5))
		#paginate class
		pagination = Grade.query.order_by(Grade.g_create_time.desc()).paginate(page,page_num)
		#get the detailed information
		grades = pagination.items

		return render_template('grade.html',pagination=pagination,grades=grades)


@user_blueprint.route('/addgrade/',methods=['POST','GET'])
@is_login
def add_grade():
	'''
	add the grade
	'''
	if request.method == 'GET':
		return render_template('addgrade.html')

	if request.method == 'POST':
		g_name = request.form.get('g_name')
		g = Grade.query.filter_by(g_name=g_name).first()

		if g:
			msg = 'class name is repeated'
			render_template('addgrade.html',msg=msg)

		grade = Grade(g_name)
		grade.save()

		return redirect(url_for('user.grade_list'))


@user_blueprint.route('/edit_grade/',methods=['POST','GET'])
@is_login
def edit_grade():
	'''
	edit the grade
	'''
	if request.method == 'GET':
		g_id = request.args.get('g_id')
		g_name = Grade.query.filter_by(g_id=g_id).first()

		return render_template('addgrade.html',g_id=g_id,g_name=g_name)

	if request.method == 'POST':
		g_id = request.form.get('g_id')
		g_name = request.form.get('g_name')

		 grade = Grade.query.filter(g_id=g_id).first()
		 grade.g_name = g_name
		 grade.save()

		 return redirect(url_for('user.grade_list'))


@user_blueprint.route('/grade_student/',methods=['GET'])
@is_login
def grade_student_list():
	'''
	the information list of the class
	'''
	if request.method == 'GET':
		g_id = request.args.get('g_id')
		stus = Student.query.filter_by(grade_id=g_id).all()

		return render_template('student.html',stus=stus)

@user_blueprint.route('/student/',methods=['GET','POST'])
@is_login
def student_list():
	'''
	stus list
	'''
	if request.method == 'GET':
		page = int(request.args.get('page',1))
		page_num = int(request.args.get('page_num',5))
		pagination = Student.query.order_by('s_id').paginate(page,page_num)
		stus = pagination.items

		return render_template('student.html',stus=stus,pagination=pagination)


@user_blueprint.route('/addstu/',methods=['GET','POST'])
@is_login
def add_stu():
	'''
	add stus
	'''
	if request.method == 'GET':
		grades = Grade.query.all()
		return render_template('addstu.html',grades=grades)

	if request.method == 'POST':
		s_name = request.form.get('s_name')
		s_sex = request.form.get('s_sex')
		grade_id = request.form.get('g_name')

		stu = Student.query.filter_by(s_name=s_name).first()
		if stu:
			msg = 'name is repeated'
			grades = Grade.query.all()
			return render_template('addstu.html',grades=grades,msg=msg)

		stu = Student(s_name=s_name,s_sex=s_sex,grade_id=grade_id)
		stu.save()

		return redirect(url_for('user.student_list'))


@







