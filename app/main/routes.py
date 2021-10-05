from flask import session, redirect, url_for, render_template, request,flash
from . import main
from .forms import LoginForm,RegisterForm
from app.Config import conn
import datetime
import json
from flask_socketio import emit
@main.route('/', methods=['GET', 'POST'])
def index():
	"""Login form to enter a room."""
	form = LoginForm()
	if form.validate_on_submit():
		login_status = check_login(form.name.data,form.password.data)
		if login_status:
			session['name'] = login_status[1]
			session['id'] = login_status[0]
			session['room'] = form.room.data
			session['created_at'] = login_status[3]
			db = conn.connection.cursor()
			db.execute("select * from fp_online_users where user_id="+str(login_status[0]))
			checkLogin=db.fetchone()
			conn.connection.commit()
			#db.close()
			#if checkLogin:

			db = conn.connection.cursor()
			db.execute("delete from  fp_online_users where user_id="+str(login_status[0]))
			conn.connection.commit()

			#db.close()
			#else:

			db = conn.connection.cursor()
			db.execute("insert into fp_online_users(name,user_id) values('"+str(login_status[1])+"','"+str(login_status[0])+"')")
			conn.connection.commit()
			#db.close()
			#return "insert into fp_online_users(name,user_id) values('"+str(login_status[1])+"','"+str(login_status[0])+"')"
			
			return redirect(url_for('.chat'))
		else:
			flash('Please check your login credentials')
			return redirect(url_for('.index'))
	elif request.method == 'GET':
		form.name.data = session.get('name', '')
		form.room.data = session.get('room', '')
	return render_template('index.html', form=form)


@main.route('/chat')
def chat():
	"""Chat room. The user's name and room must be stored in
    the session."""
	
	name = session.get('name', '')
	room = session.get('room', '')
	if name=='':
		return redirect(url_for('.index'))
		
	db = conn.connection.cursor()
	db.execute("SELECT msg.*,fu.name as name FROM fp_message as msg INNER JOIN pf_users fu on fu.id=msg.user_id where msg.created_at >=%s   order by msg.id asc ",(session['created_at']))
	messagedata=db.fetchall()
	#db.close()
	if name == '' or room == '':
		return redirect(url_for('.index'))
	return render_template('chat.html', name=name, room=room,messagedata=messagedata,onlineusers=getonlineusers())
@main.route('/logout')
def logout():
	db = conn.connection.cursor()
	db.execute("delete from fp_online_users where user_id="+str(session.get('id')))
	conn.connection.commit()
	#db.close()
	session['name']=''
	return redirect(url_for('.index'))
def check_login(uname,pwd):

	db = conn.connection.cursor()
	db.execute('select * from pf_users where email="'+str(uname)+'" and password="'+str(pwd)+'"')
	users = db.fetchone()
	#db.close()
	return users
def getonlineusers():
	newtime= datetime.datetime.now()- datetime.timedelta(minutes=2)
	beforetime= newtime.strftime('%Y-%m-%d %H:%M:%S')

	db = conn.connection.cursor()
	db.execute("select * from fp_online_users where created_at >='"+beforetime+"'")
	data = db.fetchall()
	#db.close()
	return data

@main.route('/onlineusers', methods=['GET', 'POST'])
def onlineusers():
	newtime= datetime.datetime.now()- datetime.timedelta(minutes=2)
	beforetime= newtime.strftime('%Y-%m-%d %H:%M:%S')
	dict={}
	db = conn.connection.cursor()
	db.execute("select * from fp_online_users where created_at >='"+beforetime+"'")
	data = db.fetchall()
	#db.close()
	if data:
		for row in data:
			if row[3]!='':
				dict[row[1]]=row[3]
	return json.dumps(dict)
@main.route('/register',methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		if insert_user(form):
			return redirect('/')
		else:
			return redirect('/register')
	return render_template('register.html',form=form)
def insert_user(reqst):
	email = reqst.email.data
	db = conn.connection.cursor()
	db.execute("select * from pf_users where email='" + email + "'")
	data = db.fetchone() 
	#db.close()
	if data:
		flash('Your email already exists! ' + email)
		return False

	db = conn.connection.cursor()
	id =db.execute("insert into pf_users(name,email,password,status,user_type) values('"+ reqst.name.data + "','" + email + "','" + reqst.password.data + "','1','1')")
	conn.connection.commit()
	#db.close()
	flash('Successfully Inserted !')
	return True