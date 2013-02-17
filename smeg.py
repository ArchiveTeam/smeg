#!/usr/bin/env python

import httplib
import json
import sqlite3
import sys

rangeid2 = int(sys.argv[2]) + 1

db = sqlite3.connect("posterous.sqlite", timeout=10, isolation_level=None)
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
finally:
    cursor.close()

if len(sys.argv) > 3:
    ipaddrbind = sys.argv[3]
else:
    ipaddrbind = "0.0.0.0"

conn = httplib.HTTPSConnection("posterous.com", source_address=(ipaddrbind, 0))
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "X-Xhrsource": "posterous",
    "Cookie": "_sharebymail_session_id=e55e807375f457efa9a22e091c0685c7; email=bugmenot%40trash-mail.com; _plogin=Veritas; logged_in_before=true"
}

cursor = db.cursor()
try:
    for blog_id in range(int(sys.argv[1]), rangeid2):
        cursor.execute("SELECT id FROM blog WHERE id = ?", (blog_id,))
        if cursor.fetchone():
            print "%i: already in DB" % blog_id
            continue

        print "%i: making request" % blog_id
        conn.request("GET", "/api/2/sites/%i" % blog_id, headers=headers)
        resp = conn.getresponse()
        data = resp.read()

        if resp.getheader("Connection") != "keep-alive":
            print "%i: Connection close after this request" % blog_id

        if resp.status == 200:
            data = json.loads(data)
            cursor.execute("INSERT OR REPLACE INTO blog (id, name, "
                "full_hostname, readers_count, subscribers_count, views_count, "
                "posts_count) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (data["id"], data["name"], data["full_hostname"],
                    data["readers_count"], data["subscribers_count"],
                    data["views_count"], data["posts_count"]))
        elif resp.status in [401, 404]:
            if resp.status == 404:
                print "%i: not found" % blog_id
            else:
                print "%i: password protected" % blog_id
            cursor.execute("INSERT OR IGNORE INTO blog (id) VALUES (?)", (blog_id,))
        else:
            print "%i: Unexpected HTTP status %i" % (blog_id, resp.status)
            raise Exception("Unexpected HTTP status")
finally:
    try:
        conn.close()
    except: pass
    cursor.close()
    db.close()
