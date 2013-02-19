smeg
====

[Posterous ID discovery tool](http://archiveteam.org/index.php?title=Posterous)

There are 2 options:

Normal (Shell, curl and perl)
-----------------------------
Uses HTTP, opens a connection with each request.

    ./smeg Chunk

Keep-alive (Python)
-------------------
Uses HTTPS and keep-alive. Optionally, it allows you to specify what IPv4 address to bind to (in case you have more than 1)

    ./smeg.py StartID EndID [IP to bind to]



Includes a database importer to import .hostnames

    cat *.hostnames | ./importdb.py


You can also export databases like so

    ./exportdb.py > hosts.hostnames
