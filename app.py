from marshmallow import Schema, fields, pprint
from flask import Flask, request, redirect, render_template, flash, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from hi import hi_script
from flask_wtf import Form 
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from datetime import datetime
import os

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SECRET_KEY'] = 'mchacks demo zgb 0001'

db = SQLAlchemy(app)
api = Api(app)	

class Reminder(db.Model):
	__tablename__='reminder'
	id  = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	#user = db.column(db.String(50))
	date_created = db.Column(db.DateTime)
	date_reminder = db.Column(db.String(20))
	text = db.Column(db.Text)

	def __init__(self, user, date_reminder, text, date_created=None):
		self.user_id = user
		if date_created is None:
			date_created = datetime.now()
		self.date_created = date_created
		self.date_reminder = date_reminder
		self.text = text

	def __repr__(self):
		return '<Reminder %r>' % self.text

class User(db.Model):
	__tablename__='user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True)
	reminders = db.relationship('Reminder', backref='user', lazy='dynamic')
	
	def __init__(self, username):
		self.username = username

	def __repr__(self):
		return '<User %r>' % self.username

class UserSchema(Schema):
	id = fields.Int(dump_only=True)
	username = fields.Str()

class ReminderSchema(Schema):
	id = fields.Int(dump_only=True)
	user = fields.Nested(UserSchema)
	date_created = fields.Str(dump_only=True)
	date_reminder = fields.Str()
	text = fields.Str()
	
class UsersList(Resource):
	def get(self):
		schema = UserSchema()
		json_result = schema.dump(User.query.all(), many=True)
		return json_result
	def post(self):
		raw_dict = request.get_json(force=True)
		user_dict = raw_dict['data']['attributes']
		schema = UserMessageSchema()
		try:
			schema.validate(user_dict)
			user = User(user_dict['username'])
			user.add(user)
			query = User.query.get(user.id)
			json_result = schema.dump(query)
			pprint(json_result.data)
			return json_result, 201
		except ValidationError as err:
			resp = jsonify({"error": err.messages})
			resp.status_code = 403
			return resp
		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp

class RemindersList(Resource):
	def get(self):
		schema = ReminderSchema()
		json_result = schema.dump(Reminder.query.all(), many=True)
		return json_result

#api.add_resource(GetMessages, '/api/<string:user_id>')
api.add_resource(UsersList, '/api/users')
api.add_resource(RemindersList, '/api/reminders')

#def hi_script():
#	return "yo dawg"

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
	session['username'] = request.form['username']
	q = db.session.query(User.id).filter(User.username==session['username'])
	if db.session.query(q.exists()).scalar():
		flash('User already exists')
		return redirect(url_for('home'))
	user = User(session['username'])
	db.session.add(user)
	db.session.commit()
	flash('User successfully registered')
	return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
	if not 'username' in session:
		return abort(403)
	return render_template('message.html', username=session['username'])

@app.route('/create')
def reminder_form():
	return render_template('reminder.html')

@app.route('/new', methods=['POST'])
def new_reminder():
	session['user'] = request.form['user']
	session['date'] = request.form['date']
	session['reminder'] = request.form['reminder']
	q = db.session.query(User.id).filter(User.username==session['user']).first()
	if q:
		q = q[0]
		rem = Reminder(q, session['date'], session['reminder'])
		db.session.add(rem)
		db.session.commit()
		flash('Reminder successfully created')
		return redirect(url_for('show_reminders'))
	flash('No user found')
	return redirect(url_for('reminder_form'))

@app.route('/getusers')
def show_users():
	return render_template('show_users.html', users = User.query.all())

@app.route('/getreminders')
def show_reminders():
	return render_template('show_reminders.html', reminders = Reminder.query.all())

@app.route('/hi')
def hi():
	return render_template('hi.html', hi = hi_script())

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)