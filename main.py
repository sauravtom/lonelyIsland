#!/usr/bin/env python

import flask, flask.views
app = flask.Flask(__name__)

from flask import render_template
from flask import request
import json
import os
from dbHelper import DB


@app.route('/')
def home():
    D = DB()
    arr = D.exec_query("Select * from posts")
    return flask.render_template('index.html',arr=arr,mode='normal')

@app.route('/add',methods=['GET'])
def add():
    post_title = request.args.get('post_title')
    post_url = request.args.get('post_url')
    image_url = request.args.get('image_url')
    D = DB()
    D.add_post(post_title,post_url,image_url)
    return flask.redirect("/#sa")


@app.route('/edit',methods=['GET'])
def edit():
    post_id = request.args.get('post_id')
    action = request.args.get('action')
    
    if action == 'delete':
        D = DB()
        D.delete(post_id)
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
    app.run(host='0.0.0.0')