#!/usr/bin/env python

import flask, flask.views
from settings import app, login_manager
from flask import render_template, request, url_for, abort, g
import json
import os
from dbHelper import DB
from models import *
from flask.ext.login import login_user , logout_user , current_user , login_required

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/login", methods=["GET"])
def login():
    user_name = request.args.get('user_name') or ''
    user_password = request.args.get('user_password') or ''
    if user_name and user_password:
        user_exists = User.query.filter_by(username=user_name,password=user_password).first()
        if user_exists: # user authenticated
            login_user(user_exists, remember=True)
            return flask.redirect(url_for('home'))
        else:
            registered_user = User.query.filter_by(username=user_name).first()
            if registered_user: # authentication failed
                return render_template('login.html')
            else: # new user
                user_to_be_added = User(user_password, user_name)
                db.session.add(user_to_be_added)
                db.session.commit()
                login_user(user_to_be_added, remember=True)
                return flask.redirect(url_for('home'))
    return render_template("login.html")

@app.route('/')
@login_required
def home():
    arr = Post.query.filter_by(is_deleted=0)
    print arr
    return flask.render_template('index.html',arr=arr,mode='normal')

@app.route('/view/<id>')
@login_required
def view(id):
    post = Post.query.filter_by(id=id).first()
    comments = Comment.query.filter_by(post_id=id)
    return flask.render_template('post.html',post=post, comments=comments)


@app.route('/add',methods=['GET'])
@login_required
def add():
    post_content = request.args.get('post_content')
    user_id = request.args.get('user_id')
    add_post = Post(post_content, user_id)
    db.session.add(add_post)
    db.session.commit()
    return flask.redirect("/#sa")

@app.route('/add_comment',methods=['GET'])
@login_required
def add_comment():
    comment = request.args.get('comment')
    post_id = request.args.get('post_id')
    user_id = request.args.get('user_id')
    add_comment = Comment(post_id, comment, user_id)
    db.session.add(add_comment)
    db.session.commit()
    return flask.redirect("/#sa")

@app.route('/edit',methods=['GET'])
@login_required
def edit():
    post_id = request.args.get('post_id')
    action = request.args.get('action')
    
    if action == 'delete':
        post_tobedeleted = Post.query.filter_by(id=post_id).first()
        post_tobedeleted.is_deleted = 1
        db.session.add(post_tobedeleted)
        db.session.commit()
        return flask.redirect("/#sd")

    elif action == 'edit':
        post_title = request.args.get('post_title')
        post_url = request.args.get('post_url')
        image_url = request.args.get('image_url')
        return flask.render_template('index.html',mode='update',post_url=post_url,post_title=post_title,image_url=image_url)

    elif action == 'update':
        post_title = request.args.get('post_title')
        post_url = request.args.get('post_url')
        image_url = request.args.get('image_url')
        D = DB()
        D.update(post_id,post_title,post_url,image_url)
        return flask.redirect("/#su")

    return flask.redirect("/#error")

@app.route('/logout')
def logout():
    logout_user()
    return flask.redirect(url_for('login')) 

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)