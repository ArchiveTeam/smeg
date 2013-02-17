#!/usr/bin/env python

import httplib
import json
import sqlite3
import sys

db = sqlite3.connect("posterous.sqlite")
cursor = db.cursor()
try:
    cursor.execute("SELECT * FROM blog LIMIT 1")
except sqlite3.OperationalError:
    cursor.execute("""
CREATE TABLE blog (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NULL DEFAULT NULL,
    full_hostname NULL DEFAULT NULL,
    readers_count NULL DEFAULT NULL,
    subscribers_count NULL DEFAULT NULL,
    views_count NULL DEFAULT NULL,
    posts_count NULL DEFAULT NULL
);
""")

for line in sys.stdin:
    blog_id, full_hostname = line.rstrip().split("\t", 2)
    cursor.execute("INSERT OR IGNORE INTO blog (id, full_hostname) VALUES (?, ?)", (int(blog_id), full_hostname))
db.commit()
cursor.close()
db.close()
