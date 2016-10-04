#!/usr/bin/env python

from app import app
f = open('access/ip.txt', 'r')
s = f.readline().strip()
app.run(host=s, debug = True)
