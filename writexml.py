import xml.etree.ElementTree as ET

# the following are not necessary but could be used for some special purposes
import pyperclip			# to copy stuff to clipboard
import itertools

def writeXML( seqDtRange, drange, labels, allSimOutput ):
    seqList, seqScore = makeSequence( numSpine )
    sh = allSimOutput.shape
    print "SHAPES = ", sh
    print "seqList = ", seqList
    print "seqScore = ", seqScore
    print 'LEN Labels = ', len(labels)

    assert( len(sh) == 4 and 
            sh[0] == len(seqDtRange) and 
            sh[1] == len(drange) and 
            sh[2] == len(seqList) and 
            sh[3] == len(labels) )
    root = ET.Element( 'twoDplot' )
    yaxis = ET.SubElement( root, 'yaxis' )
    yaxis.set( "title", "seqDt" )
    yaxis.text = ''.join( str(seqDt) + ' ' for seqDt in seqDtRange ) + '\n'
    xaxis = ET.SubElement( root, 'xaxis' )
    xaxis.set( "title", "distance" )
    xaxis.text = ''.join( str(d) + ' ' for d in drange ) + '\n'
    parameters = ET.SubElement( root, 'parameters' )
    p = []
    for j in params:
        p.append( ET.SubElement( parameters, j ) )
        p[-1].text = str( params[j] )

    seqOutput = ET.SubElement( root, 'seqOutput' )
    for iseq in range( len( seqList ) ):
        seqData = ET.SubElement( seqOutput, 'stimSequence' )
        seqData.set( 'index', str( iseq ) )
        seqData.set( 'score', str( seqScore[iseq] ) )
        seqData.text = ''.join( str(j) + ' ' for j in seqList[iseq] )

    simOutput = ET.SubElement( root, 'simOutput' )
    for idt in range( len( seqDtRange ) ):
        dtData = ET.SubElement( simOutput, 'dtData' )
        dtData.set( 'dt', str( seqDtRange[idt]) )
        for idistance in range( len( drange ) ):
            distanceData = ET.SubElement( dtData, 'distanceData' )
            distanceData.set( 'distance', str( drange[idistance] ) )
            for ilab in range( len( labels ) ):
                labelData = ET.SubElement( distanceData, 'labelData' )
                labelData.set( 'title', labels[ilab] )
                y = allSimOutput[idt,idistance,:,ilab]
                labelData.text = ''.join( str(j) + ' ' for j in y )

    tree = ET.ElementTree( root )
    # tree.write( fname + '.' + str( int(params['fnumber']) ) +  '.xml' )
    tree.write(fname + '_stimAmp_' + str( paramValue ) +  '.xml' )
