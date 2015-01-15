#!/usr/bin/env python

import flask, flask.views
from settings import app

from flask import render_template
from flask import request
from flask.ext.login import LoginManager
import json
import os
from dbHelper import DB
from models import *

@app.route('/')
def home():
    arr = Post.query.filter_by(is_deleted=0)
    return flask.render_template('index.html',arr=arr,mode='normal')

@app.route('/view/<id>')
def view(id):
    post = Post.query.filter_by(id=id).first()
    comments = Comment.query.filter_by(post_id=id)
    return flask.render_template('post.html',post=post, comments=comments)


@app.route('/add',methods=['GET'])
def add():
    post_content = request.args.get('post_content')
    user_id = request.args.get('user_id')
    add_post = Post(post_content, user_id)
    db.session.add(add_post)
    db.session.commit()
    return flask.redirect("/#sa")

@app.route('/add_comment',methods=['GET'])
def add_comment():
    comment = request.args.get('comment')
    post_id = request.args.get('post_id')
    user_id = request.args.get('user_id')
    add_comment = Comment(post_id, comment, user_id)
    db.session.add(add_comment)
    db.session.commit()
    return flask.redirect("/#sa")

@app.route('/edit',methods=['GET'])
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


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)