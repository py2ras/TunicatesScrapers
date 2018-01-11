#!/usr/bin/python

'''
Program to serve as reference for pie charts
@author - Sarthak Sharma <sarthaksharma@gatech.edu>
Date of Last Change - 01/11/2018
'''

import sys
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import glob

if len( sys.argv ) < 2:
    print "usage: ", sys.argv[0], ' filename_prefix'
    quit()

fileName = str(sys.argv[1])

readList = []
labelList = []

def piePlot(logFile, index):
	plotTitle = str(logFile).replace('.log','').replace('_rep2','')
	with open(logFile,'r') as fIn:
		contents = fIn.readlines()
	alignDetails = [content.strip() for content in contents]
	totalReads = int(alignDetails[1].split(' ')[0])
	unAlignedReads = int(alignDetails[2].split(' ')[0])
	uniqueAlignedReads = int(alignDetails[3].split(' ')[0])
	nonUniqueAlignedReads = int(alignDetails[4].split(' ')[0])
	overallAlignPercentage = alignDetails[5].split(' ')[0]
	data = [totalReads, unAlignedReads, uniqueAlignedReads, nonUniqueAlignedReads]
	return data, plotTitle

def main():
	fig = plt.figure(figsize=(20.5,10.5), facecolor='white')
	logFile = []
	colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'red']
	explode = (0.05,0.05,0.6,0.05,0.4) 	# explode all slices
	lines = []
	for i in range(6):
		uniqueList = []
		labelList = []
		for logFile in sorted(glob.glob(str(i+1) + "*.log")):
			data, plotTitle = piePlot(logFile,i)
			uniqueList.append(data[2])
			labelList.append(plotTitle.split('_')[1])
		ax = plt.subplot(2,3,i+1)
		lines.append(ax)
		plt.pie(uniqueList, explode=explode,autopct='%1.1f%%',colors=colors,shadow=False, startangle=90)
		plt.title(i+1,fontsize=24)
		plt.axis('equal')
	fig.subplots_adjust(hspace=0.05)
	fig.tight_layout()
	plt.legend(labelList, loc="left",bbox_to_anchor=[0.5,0.5])
	# plt.show()
	plt.savefig(str(fileName) + '.png')

if __name__ == '__main__':
	main()
