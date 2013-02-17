#!/usr/bin/env python

import httplib
import json
import sqlite3
import sys

db = sqlite3.connect("posterous.sqlite")
cursor = db.cursor()
cursor.execute("SELECT id, full_hostname FROM blog WHERE full_hostname IS NOT NULL ORDER BY id ASC")
for row in cursor:
    print "%i\t%s" % row
cursor.close()
db.close()
