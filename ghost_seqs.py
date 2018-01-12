#!/usr/bin/python

# Program to extract data from GHOST-
# online tunicates' database
# http://ghost.zool.kyoto-u.ac.jp/
# @author - Sarthak Sharma <sarthaksharma@gatech.edu>
# Date of last modification - 12/13/2017

# import the required modules
import urllib2
from bs4 import BeautifulSoup
import re
import sys
import xlsxwriter

# function to write to fasta
def writeDictToFasta(out_dict,out_file):
	with open(out_file,'w') as outFile:	
		for header,sequence in out_dict.iteritems():
			outFile.write(header)
			outFile.write(sequence)

# function to write to excel file
def writeDictToExcel(out_dict,out_file):
	workbook = xlsxwriter.Workbook(out_file)
	worksheet = workbook.add_worksheet()
	header_col0 = "SequenceName"
	header_col1 = "Sequence"
	worksheet.write(0,0,header_col0)
	worksheet.write(0,1,header_col1)
	row_num=1
	for header,sequence in out_dict.iteritems():
		worksheet.write(row_num,0,header.replace("\n","").replace(">",""))
		worksheet.write(row_num,1,sequence.replace("\n",""))
		row_num += 1
	workbook.close()
		

def writeListToFasta(out_list,out_file):
	with open(out_file,'w') as outFile:	
		for sequence in out_list:
			outFile.write(sequence)

# function to get urls from a file containing only urls - temporary (to be removed)
def get_url_from_list(lines):
	url_list = []
	for line in lines:
		url_list.append(str(line))
	return url_list

# function to get urls
def get_url_from_csv(lines):
	url_list = []
	for line in lines:
		details = line.split(',')
		transcript_id = details[2]
		url = "http://ghost.zool.kyoto-u.ac.jp/cgi-bin/fordetailkh21.cgi?name="+transcript_id+"&source=kh2013"
		url_list.append(url)
	return url_list

# function to extract data from GHOST and save as dictionary
def get_sequence(url_list):
	out_dict = {}
	#out_list = []
	for url in url_list:
		ghost_html = urllib2.urlopen(url)
		soup = BeautifulSoup(ghost_html,"lxml")
		table = soup.find("table",{"class","Table2"})
		# the nucleotide sequence is in the p tag with class "Txtbox2"		
		try:
			all_trs = table.find_all("tr")
		except AttributeError as e:
			print url
			continue
			
		# gen_var_tr: tr for nucleotide sequence with genomic variations
		gen_var_tr = all_trs[4]
		p = gen_var_tr.find("p",{"class":"Txtbox2"})
		seq = p.text.split("\n")
		header = seq[0]
		print header
		header = header + "\n"
		sequence = ("").join(strings.encode("utf-8") for strings in seq[1:])
		# certain sequences have spaces in them - should be removed
		sequence = sequence.replace(" ","")
		# replace all non-ATGC with N
		sequence = re.sub(r"[^ATGCatgc]","N",sequence)	
		sequence = sequence + "\n\n"
		out_dict[header] = sequence
	return out_dict
# main function
def main():
	# input should be a 3-column csv file with second column as the transcript ID
	if len(sys.argv) < 3:
		print "Usage ./",sys.argv[0]," <input file name> <output file name"
		quit()
	fileName = sys.argv[1]
	out_file = sys.argv[2]
	# read in the file containing transcript IDs
	with open(fileName,'rb') as inFile:
		lines = inFile.readlines()

	# construct the URLs from transcript IDs
	url_list = get_url_from_csv(lines)
	#url_list = get_url_from_list(lines)
	out_dict = get_sequence(url_list)		
	#out_list = get_sequence(url_list)
	#writeDictToFasta(out_dict,out_file)
	#writeListToFasta(out_list,out_file)
	writeDictToExcel(out_dict,out_file)

if __name__ == '__main__':
	main()
