#!/usr/bin/env python

import flask, flask.views
from settings import app, login_manager
from flask import render_template, request, url_for, abort, g, flash
import json
import os
from dbHelper import DB
from models import *
from flask.ext.login import login_user , logout_user , current_user , login_required

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/login", methods=["POST"])
def login():
    user_name = request.form.get('user_name') or ''
    user_password = request.form.get('user_password') or ''
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

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@login_required
def home():
    arr = Post.query.filter_by(is_deleted=0)
    return flask.render_template('index.html',arr=arr)

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
    if 0 < len(post_content) < 140:
        add_post = Post(post_content, user_id)
        db.session.add(add_post)
        db.session.commit()
    else:
        pass
        # flash an error message
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
    return flask.redirect("/view/%s"%post_id)

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

@app.route('/upvote_post',methods=['POST'])
@login_required
def upvote_post():
    post_id = request.form.get('post_id')
    user_id = request.form.get('user_id')
    try:
        get_post = Post.query.filter_by(id=post_id).first()
        upvoted_by = get_post.upvoted_by if get_post.upvoted_by else {}
        upvoted_by = json.loads(upvoted_by)
        if not user_id in upvoted_by:
            get_post.upvotes = get_post.upvotes + 1
            upvoted_by.append(str(user_id))
            print upvoted_by
            get_post.upvoted_by = json.dumps(upvoted_by)
            print get_post.upvoted_by
            db.session.add(get_post)
            db.session.commit()
            return ""
        else:
            # flash an error saying that user has already upvoted
            pass
    except:
        # no such post exists
        pass
    return ""


@app.route('/logout')
def logout():
    logout_user()
    return flask.redirect(url_for('login')) 

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)