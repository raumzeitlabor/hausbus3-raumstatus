#!/usr/bin/python

import os, sys
original_path = os.path.dirname(os.path.realpath(os.path.abspath(sys.argv[0])))
lib_path = original_path + '/hausbus3'
sys.path.append(lib_path)

import json
import hausbus3
from urllib2 import urlopen

import socket
socket._fileobject.default_bufsize = 0

def ohai(people):
	for person in people:
		print "OHAI " + person
		
def kthxbye(people):
	for person in people:
		print "KTHXBYE " + person

# start the Hausbus3 server on port 8080
hausbus3.start("raumstatus-proxy", http_port=8080, mqtt_broker = "127.0.0.1")

laboranten = []
laboranten_old = []

try:
	f = urlopen("http://status.raumzeitlabor.de/api/stream/full.json")
	
	for line in f: 
		if line == "\r\n": # KeepAlive-Package only
			continue
		data = json.loads(line)
		
		hausbus2.update("raumstatus","tuer",data["details"]["tuer"], False)
		hausbus2.update("raumstatus","geraete",data["details"]["geraete"], False)
		hausbus2.update("raumstatus","laboranten",data["details"]["laboranten"])
		
		laboranten_old = laboranten
		laboranten = data["details"]["laboranten"]
		
		difference = set(laboranten).symmetric_difference(set(laboranten_old))
		
		if len(difference) > 0:
			if len(laboranten) > len(laboranten_old):
				ohai(difference)
			elif len(laboranten) < len(laboranten_old):
				kthxbye(difference)
except KeyboardInterrupt:
	print '^C received, shutting down server'
finally:
	hausbus2.stop()
