#!/usr/bin/python

'''
Program to plot a heatmap from multiple xml files(very specific)
@author: Sarthak Sharma <sarthaksharma@gatech.edu>
Date of last change: 01/10/2018
'''

import sys
from matplotlib import cm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
from scipy import stats
import glob
import os
import re

if len(sys.argv) < 3:
    print "Usage: ", sys.argv[0], " outputfilename" " searchTerm" " [prefix to plotTitle]"
    quit() 
outputFileName = str(sys.argv[1])
searchTerm = str(sys.argv[2])

xmlFileList = []
for file in sorted(glob.glob("*.xml")):
    xmlFileList.append(file)	# to get all the xml files in the directory
    print file
n = len(xmlFileList) 	# n will determine how many subplots the plot is to be divided into



def plotDirectionMetric( fig, tree, index, plotTitle ):
    # Note that we are transposing X and Y axes for the matrix heatmap plot.
    #showYlabel = (index == 0) or (index == 3) or (index == 6)
    xaxis = tree.find( 'xaxis' )
    assert( xaxis != None )
    xtitle = xaxis.get( 'title' )
    
    yaxis = tree.find( 'yaxis' )
    assert( yaxis != None )
    ytitle = yaxis.get( 'title' )

    xValues = [float(j) for j in yaxis.text.split()]
    yValues = [float(j) for j in xaxis.text.split()]
    
    seqOutput = tree.find( 'seqOutput' )
    stimSequence = tree.findall( 'seqOutput/stimSequence' )
    score = { int(i.get( 'index' )):float(i.get('score')) for i in stimSequence}
    
    orderedScore = [ score[i] for i in range( len( score ) ) ]
    labelIndex = 10

    
    #################### color heatmap here ###################
    simOutput = tree.find( "simOutput" )
    aocSumAll = []
    for dtData in simOutput.iter( "dtData" ):
        for distanceData in dtData.iter( "distanceData" ):
            distance = int( distanceData.get( 'distance' ) )
            for labelData in distanceData.iter( "labelData" ):
                label = labelData.get( 'title' )
                if label == 'aocSum':
                    values = [float(q) for q in labelData.text.split()]	# [values] stores the aocSum values
                    # aocSumAll.append( (values[0] - np.mean( values) ) / max( values ) )
                    aocSumAll.append( (values[0] - values[-1]) / max( values[0],values[-1] ) )
    ax = plt.subplot(2,5,index+1)
    ax.tick_params( direction = 'out', labelsize=18 )
    d = np.array( aocSumAll)
    md = min(0.0, min( d ))
    # This has two problems: The axes are transposed, and the ordering of
    # the entries for time (in the columns; xValues) are flipped.
    d.shape = (len( xValues ), len( yValues ) )
    td0 = [ i[::-1] for i in d ] # Unflip the time ordering
    td = np.transpose( td0 )     # Put time on the x axis, dist on y axis.
    cax = plt.imshow( td, cmap = cm.jet, vmin = -1, vmax=1, interpolation='none' )
    
    if len(sys.argv) == 4:
     	plt.title(str(sys.argv[3] + plotTitle))
    else:
     	plt.title(plotTitle)

    if index == 0 or index == 5:
    	plt.ylabel( r"Spine Spacing ($\mu$m)", fontsize = 18)
    plt.xlabel( "Time (s)", fontsize = 18 )
    xticks = [str(int(x)) for x in xValues]
    plt.xticks ( range( len(xValues ) ), xticks )
    plt.yticks( range( len(yValues)-1, -1, -1 ), [str(y/5) for y in yValues] )
    return cax

def main():
    caxList = []
    fig = plt.figure( figsize = (20.5,10.5), facecolor='blue')
    for index,xmlFile in enumerate(xmlFileList):
    	bisTree = ET.parse( xmlFile )
    	plotTitle = str(xmlFile).replace(searchTerm,'').replace('.xml','').replace('_','-')
    	cax = plotDirectionMetric( fig, bisTree, index, plotTitle )
    fig.subplots_adjust(hspace=0.05)
    # fig.tight_layout()
    # fig.subplots_adjust(right=0.8)
    # fig.subplots(squeeze=False)
    
    cbar_ax = fig.add_axes([0.05,0.05,0.9,0.025])
    cbar = fig.colorbar( cax, cax=cbar_ax, orientation='horizontal' )
    cbar.ax.tick_params(labelsize=18)
    plt.suptitle( outputFileName, fontsize=20 )

    plt.savefig( outputFileName + ".png" )

if __name__ == '__main__':
    main()
