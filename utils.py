# -*- coding: utf-8 -*-
# vim:set ts=8 sts=8 sw=8 tw=80 noet cc=80:

from random import randrange as random

def oneof(values):
	return values[random(len(values))]

def startswith(a, b):
	if len(b) > len(a):
		return False
	if len(b) == 0:
		return True
	for i in range(len(b)):
		if a[i] != b[i]:
			return False
	return True

def load_database(filename):
	database = {}
	with open(filename, "r") as f:
		for line in f.readlines():
			line = line.strip()
			parts = line.split(";")
			key = parts[0].strip().lower()
			value = ";".join(parts[1:]).strip()
			database[key] = value
	return database
