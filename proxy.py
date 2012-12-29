#!/usr/bin/python

import os, sys
original_path = os.path.dirname(os.path.realpath(os.path.abspath(sys.argv[0])))
lib_path = original_path + '/hausbus2'
sys.path.append(lib_path)

import json
import hausbus2
from urllib2 import urlopen

import socket
socket._fileobject.default_bufsize = 0

def ohai(people):
	for person in people:
		print "OHAI " + person
		
def kthxbye(people):
	for person in people:
		print "KTHXBYE " + person

f = urlopen("http://status.raumzeitlabor.de/api/stream/full.json")

laboranten = []
laboranten_old = []

for line in f: 
	if line == "\r\n": # KeepAlive-Package only
		continue
	
	laboranten_old = laboranten
	laboranten = json.loads(line)["details"]["laboranten"]
	
	difference = set(laboranten).symmetric_difference(set(laboranten_old))
	
	if len(difference) > 0:
		if len(laboranten) > len(laboranten_old):
			ohai(difference)
		elif len(laboranten) < len(laboranten_old):
			kthxbye(difference)


