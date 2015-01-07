#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os
import hashlib
import json
import requests

class DB(object):
    
    file_name = 'data.db'

    def __init__(self):
        self.conn = sqlite3.connect(self.file_name, check_same_thread=False)
        self.c = self.conn.cursor()
        self.create_posts_table()
        self.create_comments_table()

    @classmethod
    def getdbpath(cls):
        return os.path.abspath(cls.file_name)

    def create_posts_table(self):
        # create new db and make connection
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS posts (post_id TEXT UNIQUE,user_id TEXT, text TEXT UNIQUE,upvotes NUMBER,upvoted_by TEXT)''')
        self.conn.commit()

    def create_comments_table(self):
        # create new db and make connection
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS comments (comment_id TEXT UNIQUE,comment TEXT, post_id TEXT,user_id TEXT )''')
        self.conn.commit()
    
    def add_post(self,text,user_id="admin"):
        post_id = hashlib.md5(text).hexdigest()[:6]
        upvotes = 0
        upvoted_by = ''
        
        try:
            self.c.execute(
                "INSERT INTO posts VALUES (?,?,?,?,?)",
                (post_id,user_id,text,upvotes,upvoted_by))
            self.conn.commit()
        except:
            print "Values already present in DB"

    def add_comment(self,comment,post_id,user_id='admin'):
        comment_id = hashlib.md5(comment+post_id).hexdigest()[:6]

        try:
            self.c.execute(
                "INSERT INTO comments VALUES (?,?,?,?)",
                (comment_id,comment,post_id,user_id))
            self.conn.commit()
        except:
            print "Values already present in DB"


    def delete(self,id,type):
        if type == 'post':
            self.c.execute("DELETE from posts where post_id like '%s';"%id)
        if type == 'comment':
            self.c.execute("DELETE from comments where comment_id like '%s';"%id)
        self.conn.commit()

    def exec_query(self, query):
        result_arr = []
        try:
            self.c.execute(query)
            for row in self.c:
                result_arr.append(row)
        except:
            result_arr = []
        return result_arr


def test():
    D =DB()
    D.add_post("We all live in a yellow submarine.")
    D.add_comment("Hello there","dc4fec")
    #D.exec_query("delete from links where _id like '%s'"%post_id)
    #D.add_to_db('Motivational Title','article url','image url')
    #D.update('f9c88c','foo','foo','foo')
    #D.delete('542fb0')


if __name__ == '__main__':
    test()

