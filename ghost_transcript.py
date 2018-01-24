#!/usr/bin/python

# Program to extract transcript IDs
# online database for C. intestinalis:
# http://ghost.zool.kyoto-u.ac.jp/
# @author - Sarthak Sharma <sarthaksharma@gatech.edu>
# Date of last modification - 12/18/2017

# import the required modules
import urllib2
from bs4 import BeautifulSoup
import re
import sys

# function to write to csv file
def writeListToCsv(lines,out_list,out_file):
	with open(out_file,'w') as outFile:
		for i,transcript_id in enumerate(out_list):
			if i == 0:
				outFile.write(lines[i].replace("\n","")+",Transcript IDs"+"\n")
			else:
				outFile.write(lines[i].replace("\n","")+","+transcript_id)
				outFile.write("\n")

# function to get urls from csv file;
# col_num - the column number in the csv file which
# should be used to create urls
def get_url_from_csv(lines,col_num):
	url_list = []
	for line in lines:
		details = line.split(',')
		kh_id = details[col_num]
		kh_id = kh_id.replace('"','')
		url = "http://ghost.zool.kyoto-u.ac.jp/cgi-bin/fordetailkh21.cgi?name="+kh_id+";source=kh2013"
		url_list.append(url)
	return url_list

# function to get transcript ids from GHOST and save as dictionary
def get_transcript_ids(url_list):
	out_list = []
	for url in url_list:
		ghost_html = urllib2.urlopen(url)
		soup = BeautifulSoup(ghost_html,"lxml")
		table = soup.find("table",{"class","Table1"})
		try:
			all_trs = table.find_all("tr")
		except AttributeError as e:
			print url
			out_list.append("None")			# appending None so that number of elements remain the same in the input and output file
			continue
		# variants_tr: tr for with the list of variant IDs - the last one
		variants_tr = all_trs[-1]
		# a_list: list of 'a' tags in the HTML - they are all actually references to new webpages
		a_list = variants_tr.find_all("a")
		try:
			transcript_id = a_list[-1].text		# we need the last one for now - might be changed
		except IndexError as e:
			print url
			continue
		out_list.append(transcript_id)
	return out_list

# main function
def main():
	# input should be a csv file with KH IDs
	if len(sys.argv) < 4:
		print "Usage: ",sys.argv[0]," <input file name> <output file name> <column number with KH IDs>"
		quit()
	fileName = sys.argv[1]
	out_file = sys.argv[2]
	col_num = int(sys.argv[3]) - 1
	# read in the file containing KH IDs
	with open(fileName,'r') as inFile:
		lines = inFile.readlines()

	# construct the URLs from KH IDs
	url_list = get_url_from_csv(lines,col_num)
	out_list = get_transcript_ids(url_list)
	print out_list
	#writeListToCsv(lines,out_list,out_file)

if __name__ == '__main__':
	main()
