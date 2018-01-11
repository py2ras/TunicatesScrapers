#!/usr/bin/python

'''
Program to read Bowtie Logs which have been saved to files
And plot the information from them
This is for stepwise-subtractive-mapping logs plot.
Use this from respective directories of structural RNA alignments.
@author - Sarthak Sharma <sarthaksharma@gatech.edu>
Date of Last Change - 01/11/2018
'''

import sys
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import glob

logFileList = []

if len( sys.argv ) < 2:
    print "usage: ", sys.argv[0], ' filename_prefix'
    quit()

fileName = str(sys.argv[1])

for logFile in sorted(glob.glob("*.log")):
	logFileList.append(logFile)
	print logFile
n = len(logFileList)


ind = np.arange(0, n*2, 2)
width = 0.5

readList = []
labelList = []
def main():
	fig = plt.figure( figsize=(20.5,10.5), facecolor='white')
	for index,logFile in enumerate(logFileList):
		plotTitle = str(logFile).replace('.log','').replace('_rep2','')
		labelList.append(plotTitle)
		with open(logFile,'r') as fIn:
			contents = fIn.readlines()
		alignDetails = [content.strip() for content in contents]
		totalReads = int(alignDetails[1].split(' ')[0])
		unAlignedReads = int(alignDetails[2].split(' ')[0])
		uniqueAlignedReads = int(alignDetails[3].split(' ')[0])
		nonUniqueAlignedReads = int(alignDetails[4].split(' ')[0])
		overallAlignPercentage = alignDetails[5].split(' ')[0]
		data = [totalReads, unAlignedReads, uniqueAlignedReads, nonUniqueAlignedReads]
		readList.append(data)
	ax = plt.subplot(111)
	ax.bar(ind, [data[0] for data in readList],width,color='r',label='Total')
	ax.bar(ind+width, [data[1] for data in readList],width,color='b',label='Unaligned')
	ax.bar(ind+2*width, [data[2] for data in readList],width,color='y',label='Unique')
	ax.bar(ind+3*width, [data[3] for data in readList],width,color='g',label='Non-unique')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(labelList)
	rects = ax.patches
	print len(rects)
	names = ("Total", "Unaligned", "Unique", "Non-unique")
	ax.legend()
	for i,rect in enumerate(rects):
		height = rect.get_height()
		ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
			'%d' %int(height), 
			ha='center',va='bottom', rotation=25)
	plt.savefig(fileName + ".png")
	# plt.show()

if __name__ == '__main__':
	main()
