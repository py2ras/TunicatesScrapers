#!/usr/bin/python

'''
Program to convert csv format to fasta format
@author: Sarthak Sharma <sarthaksharma@gatech.edu>
Date of last change: 01/10/2018
'''


import sys

def main():
	if len(sys.argv) < 2:
		print "Usage: ./",sys.argv[0]," <input csv>"
		quit()
	fileName = sys.argv[1]
	out_file = fileName[:-4]+".fa"
	with open(fileName,"r") as inFile:
		lines = inFile.readlines()
	
	with open(out_file,"w") as outFile:
		for line in lines:
			details = line.split(',')
			header = details[2]
			sequence = details[4]
			outFile.write(header)
			outFile.write("\n")
			outFile.write(sequence)
			outFile.write("\n")
	
if __name__ == '__main__':
	main()
			
