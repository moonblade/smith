#!/bin/python
import sys
import random

permissibleCharacters=['A','U','G','C']
numberOfDataEntries=int(sys.argv[1])
minLength=5
maxLength=50
file=open('data.csv','w')
file.write('seq1,seq2'+"\n")
for x in range(numberOfDataEntries):
	length=random.randint(minLength,maxLength)
	seq1=''.join(random.choice(permissibleCharacters) for _ in range(length))	
	seq2=''.join(random.choice(permissibleCharacters) for _ in range(length))	
	line = seq1+","+seq2
	file.write(line+"\n")
file.close()