import os, sys
def toUpper(fileName):
	with open(fileName, "r+b") as file:
		content = file.read()
		file.seek(0)
		file.write(content.upper())