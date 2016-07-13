#!/usr/bin/python3 -u
# Plounge comment and submission gathering bot

import time
import sqlite3
import re

import praw
from praw.errors import APIException, HTTPException

# This causes praw to print out all requests. Useful for debugging.
# import logging
# logging.basicConfig(level=logging.DEBUG)

class PloungeDB:
  def __init__(self, filename):
    self.filename = filename
    self.db = None

  def __enter__(self):
    self.db = sqlite3.connect(self.filename)
    self.db.execute("""CREATE TABLE IF NOT EXISTS submissions (
      id TEXT NOT NULL PRIMARY KEY UNIQUE,
      author TEXT,
      title TEXT,
      selftext TEXT,
      url TEXT,
      udate DATE NOT NULL,
      permalink TEXT
    )""")
    self.db.execute("""CREATE TABLE IF NOT EXISTS comments (
      id TEXT NOT NULL PRIMARY KEY UNIQUE,
      parent_id TEXT,
      author TEXT,
      body TEXT,
      udate DATE NOT NULL,
      permalink TEXT
    )""")
    return self

  def __exit__(self, t, value, tb):
    self.db.close()

  def insert_comment(self, c):
    # the OR IGNORE may be removed in the future, if I can be reasonably
    # certain, that reddit won't give me duplicates
    query = """INSERT OR IGNORE INTO comments (
        id, parent_id, author, body, udate, permalink
      ) VALUES ( ?, ?, ?, ?, ?, ? )"""
    created = time.strftime("%Y-%m-%d %X", time.gmtime(c.created_utc))
    author = c.author.name if c.author != None else "[deleted]"
    # for some reason, the comment listing does not contain the permalink, even
    # though it is really simple to derive frome what we have
    permalink = ''.join(["https://www.reddit.com/r/MLPLounge/comments/",
                         c.link_id[3:],
                         "/",
                         re.sub('[^a-zA-Z0-9]', '_', c.link_title).lower(),
                         "/",
                         c.id])
    data = (c.fullname, c.parent_id, author, c.body, created, permalink)
    self.db.execute(query, data)
    return data

  def insert_submission(self, s):
    # basically the same as for the comments
    query = """INSERT OR IGNORE INTO submissions (
        id, title, author, selftext, url, udate, permalink
      ) VALUES ( ?, ?, ?, ?, ?, ?, ? )"""
    created = time.strftime("%Y-%m-%d %X", time.gmtime(s.created_utc))
    author = s.author.name if s.author != None else "[deleted]"
    data = (s.fullname, s.title, author, s.selftext, s.url, created, s.permalink)
    self.db.execute(query, data)
    return data

  def commit(self):
    self.db.commit()

def main():
  with PloungeDB('data/plounge.db') as db:
    print("Starting plounge comment gatherer")
    sub = praw.Reddit('mlplounge.science data collector') \
              .get_subreddit('mlplounge')
    # this variable limits the number of comments/submissions that get
    # retrieved during an iteration. 0 means that the default limit for one
    # page is used. None means that the maximum possible number of results is
    # returned.
    limit = None
    while True:
      try:

        comments = sub.get_comments(limit=limit)
        for c in comments:
          (cid, cpid, author, body, created, permalink) \
                  = db.insert_comment(c)

        submissions = sub.get_new(limit=limit)
        for s in submissions:
          (sid, title, author, text, url, created, link) \
                  = db.insert_submission(s)

        # save the state of the database
        db.commit()

        # Reddit doesn't want you to request the same page more than
        # once every 30 secons. I technically don't request the same
        # page but it is probably a good idea anyway
        time.sleep(31)
        # Updates after the first one will be rather small, we can
        # therefore set the limit to 0 to always get as many things
        # as possible with a single query. Previously, there was a
        # system to only get comments after the last inserted one but
        # that turned out to be unreliable due to the fact that you
        # can't continue a list from a deleted comment or shit like
        # that. Another explanation would be that the after's expire
        # after a certain time, I don't know. Getting a fixed number
        # of comments each iteration is ugly but seemingly necessary.
        limit = 0
      except (APIException, HTTPException):
        print("Got an (probably temporary) exception from praw.")
        print("Delaying for 30 seconds")
        # We don't know how many comments we have potentially lost.
        # Get the maximum number just to be sure
        limit = None
        time.sleep(30)

if __name__ == '__main__':
  main()
