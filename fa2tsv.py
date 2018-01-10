#!/usr/bin/python

# Program to convert fasta files to tsv format
# @author: Sarthak Sharma
# Date of last change: 01/10/2018

import sys

def main():
	fileName = sys.argv[1]
	outFile = fileName[:-3] + ".tsv"
	with open(fileName) as inFile:
		lines = inFile.readlines()
	
	length = len(lines)
	with open(outFile,"w") as outFile:
		for i in range(0,length,3):
			outFile.write(lines[i].replace("\n",""))
			outFile.write("\t")
			outFile.write(lines[i+1].replace("\n",""))
			outFile.write("\n")

if __name__ == '__main__':
	main()
