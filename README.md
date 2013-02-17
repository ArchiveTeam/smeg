smeg
====

Posterous ID discovery tool

There are 2 options:

Normal (Shell, curl and perl)
-----------------------------
Uses HTTP, opens a connection with each request.

>./smeg Chunk

Keep-alive (Python)
-------------------
Uses HTTPS and keep-alive. Optionally, it allows you to specify what IPv4 address to bind to (in case you have more than 1)

>./smeg.py StartID EndID [IP to bind to]

Includes a database importer to import .hostnames
>cat *.hostnames | ./importdb.py

You can also export databases like so
>./exportdb.py > hosts.hostnames




It is possible to run multiple smeg instances using
>for chunk in $(seq 900 999); do ./smeg.py ${chunk}000000 ${chunk}999999 & done
if you were doing the 9m range.
This, however, will cause conflits with the Python version, due to the usage of sqlite.
