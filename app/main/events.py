from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from app.Config import conn
import datetime

@socketio.on('joined', namespace='/chat')
def joined(message):
	"""Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
	room = session.get('room')
	join_room(room)
	if session.get('id'):
		datadate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		db = conn.connection.cursor()
		sql = 'update fp_online_users set created_at=%s where user_id=%s'
		db.execute(sql,(datadate,str(session.get('id'))))
		conn.connection.commit()
	#db.close()
	#onlineuser='<li class="online_users" id="user'+session.get('id')+'"> <span>'+session.get('name')+' </span></li>'
	emit('status', {'msg': str(session.get('name')) + ' has entered the room.','name': str(session.get('name')),'userid':str(session.get('id')),'dataid':5}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
	"""Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
	if message['msg']:
		datadate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		db = conn.connection.cursor()
		db.execute("select * from fp_online_users where user_id="+str(session.get('id')))
		if db.fetchone():
			db = conn.connection.cursor()
			sql = 'update fp_online_users set created_at=%s where user_id=%s'
			db.execute(sql,(datadate,str(session.get('id'))))
			conn.connection.commit()
		else:
			db = conn.connection.cursor()
			db.execute("insert into fp_online_users(name,user_id) values('"+str(session.get('name'))+"','"+str(session.get('id'))+"')")
			conn.connection.commit()
		#db.close()

		db = conn.connection.cursor()
		sql='insert into fp_message(message,user_id) values(%s,%s)'
		db.execute(sql,(message['msg'],session.get('id')))
		conn.connection.commit()
		#db.close()
	room = session.get('room')
	emit('message', {'msg':'<div class="chatlist"><span class="name">'+session.get('name')+' : </span><div class="msg">'+message['msg']+'</div></div>','name':session.get('name')}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.','name': session.get('name'),'userid':session.get('id'),'dataid':1}, room=room)

