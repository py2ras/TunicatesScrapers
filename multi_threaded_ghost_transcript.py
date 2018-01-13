#!/usr/bin/python

# Program to extract transcript IDs
# online database for C. intestinalis:
# http://ghost.zool.kyoto-u.ac.jp/
# This script utilises basic multithreading - just enough for the time-being
# [NOTE] The multithreading might change in future
# @author - Sarthak Sharma <sarthaksharma@gatech.edu>
# Date of last modification - 01/11/2018

# import the required modules
import urllib2
from bs4 import BeautifulSoup
import re
import sys
from multiprocessing.dummy import Pool as ThreadPool

# function to write to csv file
def writeListToCsv(lines,out_list,out_file):
	with open(out_file,'w') as outFile:
		for i,line_text in enumerate(out_list):
			outFile.write(line_text)
			outFile.write("\n")
			

# function to get urls from csv file;
# col_num - the column number in the csv file which
# should be used to create urls
def get_url_from_csv(lines,col_num):
	line_list = []
	for line in lines:
		details = line.split(',')
		kh_id = details[col_num]
		kh_id = kh_id.replace('"','')
		url = "http://ghost.zool.kyoto-u.ac.jp/cgi-bin/fordetailkh21.cgi?name="+kh_id+";source=kh2013" 
		details.append(url)
		line_list.append(details)
	return line_list

# function for multithreading
def multi(line_list):
	pool = ThreadPool(4)
	out_list = pool.map(get_transcript_ids,line_list)
	pool.close()
	pool.join()
	return out_list

# function to get transcript ids from GHOST and save as dictionary
def get_transcript_ids(line):
	#out_list = []
	url = line[-1]	
	try:
		ghost_html = urllib2.urlopen(url)
		soup = BeautifulSoup(ghost_html,"lxml")
		table = soup.find("table",{"class","Table1"})
	except ValueError as e:
		return "None"+url
	try:
		all_trs = table.find_all("tr")
	except AttributeError as e:
		return "None"+url
		#out_list.append("None")			# appending None so that number of elements remain the same in the input and output file
	try:
		# variants_tr: tr for with the list of variant IDs - the last one
		variants_tr = all_trs[-1]
		# a_list: list of 'a' tags in the HTML - they are all actually references to new webpages
		a_list = variants_tr.find_all("a")
		transcript_id = a_list[-1].text		# we need the last one for now - might be changed
		#out_list.append(transcript_id)
		temp_line = line[0:3]
		temp_line.append(transcript_id)
		text = ','.join(temp_line)
		text = text.replace('\n','')
	except IndexError as e:
		return "None"+url
	return text 
	#return out_list

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
	line_list = get_url_from_csv(lines,col_num)
	out_list = multi(line_list)
	writeListToCsv(lines,out_list,out_file)

if __name__ == '__main__':
	main()
