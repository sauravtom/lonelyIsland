from flask.ext.sqlalchemy import SQLAlchemy
# from sqlalchemy import Table, Column, Float, Integer, String, MetaData, Text, Boolean, ForeignKey
from flask import Flask
from settings import app, db

class TimeStampedModel(db.Model):
	__abstract__ = True
	created = db.Column(db.DateTime, default=db.func.now())
	modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class User(TimeStampedModel):
	__table_args__ = {'extend_existing': True}
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	password = db.Column(db.Text)
	email = db.Column(db.String(120), unique=True, nullable=True)
	post_ids = db.Column(db.String, default=None)
	is_deleted = db.Column(db.Boolean, default=False)
	posts = db.relationship('Posts', backref='users', lazy='dynamic')
	comments = db.relationship('Comment', backref='users', lazy='dynamic')

	def __init__(self, password, email=None, post_ids=None):
		self.password = password
		self.email = email
		self.post_ids = post_ids

	def __repr__(self):
	    return '<User %r>' % self.email

class Posts(TimeStampedModel):
	__table_args__ = {'extend_existing': True}
	__tablename__ = 'posts'

	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text)
	image = db.Column(db.Text, nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	upvotes = db.Column(db.Integer, default=0)
	upvoted_by = db.Column(db.String, default=None)
	is_deleted = db.Column(db.Boolean, default=False)
	comments = db.relationship('Comment', backref='posts', lazy='dynamic')

	def __init__(self, content, user_id, image=None, upvotes=0, upvoted_by=None):
		self.content = content
		self.user_id = user_id
		self.image = image
		self.upvotes = upvotes
		self.upvoted_by = upvoted_by
	
	def __repr__(self):
		return 'content %s' % self.content

	def get_all_posts(self):
		return Post.query.all()

	def get_all_posts_user(self, user_id):
		return Post.query.filter_by(user_id=user_id)

class Comment(TimeStampedModel):
	__table_args__ = {'extend_existing': True}
	__tablename__ = 'comments'

	id = db.Column(db.Integer, primary_key=True)
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
	content = db.Column(db.Text)
	image = db.Column(db.Text, nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	upvotes = db.Column(db.Integer, default=0)
	upvoted_by = db.Column(db.String, default=None)
	is_deleted = db.Column(db.Boolean, default=False)

	def __init__(self, content, user_id, image=None, upvotes=0, upvoted_by=None):
		self.content = content
		self.user_id = user_id
		self.image = image
		self.upvotes = upvotes
		self.upvoted_by = upvoted_by

	def __repr__(self):
		return 'content %s' % self.content

	def get_all_comments_post(self, post_id):
		return Comment.query.filter_by(post_id=post_id)

	def get_all_comments_user(self, user_id):
		return Comment.query.filter_by(user_id=user_id)