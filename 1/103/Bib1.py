import sys

CODEV = len(sys.argv)>1 and sys.argv[1] == "CODEV"

def printCodev(msg):
	global CODEV
	if not CODEV:
		print(msg)

def entrada():
	x = input().strip()
	while(x == ""):
		x = input().strip()
	return x