#!/usr/bin/python

'''
Program to plot bar charts from xml files (specific)
@author: Sarthak Sharma <sarthaksharma@gatech.edu>
Date of last change: 01/10/2018
'''
# [FIX ME] This program has a lot of hard-coded stuff. If it's needed in further analysis, clean it.

import sys
import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET

if len( sys.argv ) < 2:
    print "usage: ", sys.argv[0], ' xml filename'
    quit()

tree = ET.parse( sys.argv[1] )

#caDistance = tree.find( "caDistance" )
#caDistanceList = []
#patternList = []
#for distance in caDistance.iter( "distance" ):
#	patternList.append( distance.get( 'pattern' ) )
#	caDistanceList.append([int(q) for q in distance.text.split()])

parameters = tree.find( "parameters" )
zList = parameters.find( "zList" )
zvals = zList.text
stampl = parameters.find( 'stimAmplitude' )
ampl = stampl.text


simOutput = tree.find( "simOutput" )
aocList = []
peakList = []
peakLabList = []
aocLabList = []
for dtData in simOutput.iter("dtData"):
	for distanceData in dtData.iter( "distanceData" ):
		for labelData in distanceData.iter( "labelData" ):
			label = labelData.get( 'title' )
			values = [float(q) for q in labelData.text.split()]
			if label[:3] == 'aoc':
				aocLabList.append(label)
				aocList.append(values)
			if label[:4] == 'peak':
				peakLabList.append(label)
				peakList.append(values)

ind = np.arange(0, (len(aocList)-1)*2, 2)
width = 0.35

#fig = plt.figure( figsize = (18.5,10.5), facecolor='white')
fig = plt.figure( figsize = (18.5,10.5), facecolor='blue')

axAocSum = plt.subplot2grid((2,2), (0,0), rowspan=2)
rectsAS1 = axAocSum.bar(0, [i[0] for i in aocList][-1], width, color='r' )
rectsAS2 = axAocSum.bar(0+width, [i[1] for i in aocList][-1], width, color='y')
rectsAS3 = axAocSum.bar(0+2*width, [i[2] for i in aocList][-1], width, color='g')
axAocSum.set_ylabel('Areas Sum')
#axAocSum.set_title('Area_Sum_spacing-%s_zList-%s-ampl-%s' %(''.join(str(dis) + '-' for dis in caDistanceList[0]), zvals, ampl) )
axAocSum.set_xlabel('aocSum')
axAocSum.set_xticklabels([])
axAocSum.legend( (rectsAS1[0], rectsAS2[0], rectsAS3[0]), tuple(patternList) )

axAoc = plt.subplot2grid((2,2), (0,1))
rectsA1 = axAoc.bar(ind, [i[0] for i in aocList][:-1], width, color='r' )
rectsA2 = axAoc.bar(ind+width, [i[1] for i in aocList][:-1], width, color='y')
rectsA3 = axAoc.bar(ind+2*width, [i[2] for i in aocList][:-1], width, color='g')
axAoc.set_ylabel('Areas')
#axAoc.set_title('Area comparison-%s_zList-%s-ampl-%s' %(''.join(str(dis) + '-' for dis in caDistanceList[0]), zvals, ampl) )
axAoc.set_xticks(ind + width)
axAoc.set_xticklabels(aocLabList[0:-1])
# axAoc.legend( (rectsA1[0], rectsA2[0], rectsA3[0]), tuple(patternList) )

axPeak = plt.subplot2grid((2,2), (1,1))
rectsP1 = axPeak.bar(ind, [i[0] for i in peakList][:-1], width, color='r' )
rectsP2 = axPeak.bar(ind+width, [i[1] for i in peakList][:-1], width, color='y')
rectsP3 = axPeak.bar(ind+2*width, [i[2] for i in peakList][:-1], width, color='g')
axPeak.set_ylabel('Peaks')
#axPeak.set_title('Peak comparison-%s_zList-%s-ampl-%s' %(''.join(str(dis) + '-' for dis in caDistanceList[0]), zvals, ampl) )
axPeak.set_xticks(ind + width)
axPeak.set_xticklabels(peakLabList[0:-1])
# axPeak.legend( (rectsP1[0], rectsP2[0], rectsP3[0]), tuple(patternList))


# plt.show()
#plt.savefig("fig_diffZ-"+ str(zvals) + "_spacing-" + ''.join(str(dis) + '-' for dis in caDistanceList[0]) + "ampl-" + str(ampl) + ".png")

plt.savefig("fig_diffZ-"+ str(zvals) + "_spacing-" + "ampl-" + str(ampl) + ".png")
