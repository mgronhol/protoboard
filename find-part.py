#!/usr/bin/env python

import json, sys


entry = sys.argv[1].lower()

parts = {}

with open( "parts.json", "r" ) as handle:
	parts = json.loads( handle.read() )


keys = parts.keys()

maxlen = max( len(k) for k in keys) 

fmt = "%" + str( maxlen + 1 ) + "s"


for key in keys:
	if entry in key.lower():
		print fmt%key, "\t", parts[key]["description"]
