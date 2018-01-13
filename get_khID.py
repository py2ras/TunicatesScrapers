#!/usr/bin/python

# Program to get KHIDs from Unique Names
# Required because Seurat outputs a list of Unique Names
# This will read the markers lists and return a list with the corresponding Transcript IDs

import sys
import getopt

# function to parse options
def parse_options():
	options,remainder = getopt.gnu_getopt(sys.argv[1:], 'i:c:f:u:k:t:',['input_uniq=','col1uniq=','input_kh_trid=','col2uniq=','col2khid=','col2trid='])
	# print "OPTIONS: ", options
	for opt,arg in options:
		if opt in ('-i','--input_uniq'):
			input_uniq = arg
		elif opt in ('-c','--col1uniq'):
			col1uniq = int(arg)-1
		elif opt in ('-f','--input_kh_trid'):
			input_kh_trid = arg
		elif opt in ('-u','col2uniq'):
			col2uniq = int(arg)-1
		elif opt in ('-k','col2khid'):
			col2khid = int(arg)-1
		elif opt in ('-t','col2trid'):
			col2trid = int(arg)-1
	ext_ind = input_uniq.index(".")
	output_file = input_uniq[:ext_ind] + "_kh_tr"
	return input_uniq, col1uniq, input_kh_trid, col2uniq, col2khid, col2trid, output_file

# define the usage function
def usage():
	print '\033[1m'+"Usage: "+ sys.argv[0]+'\033[0m', "[OPTIONS]"
	print '\033[1m'
	print "OPTIONS:"
	print "\t-i, --input_uniq=FILE"+'\033[0m'
	print "\t\tinput csv file name with the Unique names"
	print '\033[1m'
	print "\t-c, --col1uniq=INT"+'\033[0m'
	print "\t\tcolumn number with the Unique names in file i"
	print '\033[1m'
	print "\t-f, --input_kh_trid=FILE"+'\033[0m'
	print "\t\tinput csv file name with the Unique names, KH IDs and transcript IDs"
	print '\033[1m'
	print "\t-u, --col2uniq=INT"+'\033[0m'
	print "\t\tcolumn number with the Unique names in file f"
	print '\033[1m'
	print "\t-k, --col2khid=int"+'\033[0m'
	print "\t\tcolumn number with the KH IDs in file f"
	print '\033[1m'
	print "\t-t, --col2trid=INT"+'\033[0m'
	print "\t\tcolumn number with the Transcript IDs in file f"
	print '\033[1m'
	print "RETURN"+'\033[0m'
	print "\tThe output file will have the same columns as the input file with 2 additional columns one each for KH IDs and Transcript IDs"
	print "\tand the output csv file be named same as the file f with '_kh_tr' suffix."  
	quit()

# function to write to output csv file
def write2csv(out_list,output_file):
	output_file = output_file + ".csv"
	with open(output_file,'w') as outFile:
		for out_line in out_list:
			outFile.write(out_line)

# function to compare the 2 csv files
# and get the KHIDs and Transcript IDs
def get_kh_trids(lines_uniq,lines_kh_trid):
	out_list = []
	for line1 in lines_uniq[1:]:
		details1 = line1.split(",")
		uniq_name1 = details1[col1uniq]
		for line2 in lines_kh_trid[1:]:
			details2 = line2.split(",")
			uniq_name2 = details2[col2uniq]
			kh_id = details2[col2khid]
			tr_id = details2[col2trid].replace("\n","")
			if uniq_name1 == uniq_name2:
				out_line = kh_id + ',' + tr_id + ',' + line1
				out_list.append(out_line)
	return out_list
def main():
	global col1uniq,col2uniq,col2khid,col2trid
	if len(sys.argv) < 13:
		usage()
	input_uniq, col1uniq, input_kh_trid, col2uniq, col2khid, col2trid, output_file = parse_options()
	with open(input_uniq,'r') as in1:
		lines_uniq = in1.readlines()
	with open(input_kh_trid,'r') as in2:
		lines_kh_trid = in2.readlines()
	out_list = get_kh_trids(lines_uniq,lines_kh_trid)
	write2csv(out_list,output_file)
		
if __name__ == '__main__':
	main()

