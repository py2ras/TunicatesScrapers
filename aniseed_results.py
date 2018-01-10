#!/usr/bin/python

# Program to extract data from ANISEED-
# an online Tunicate gene expression database
# www.aniseed.cnrs.fr
# @author - Sarthak Sharma <sarthaksharma@gatech.edu>
# Date of last modification - 12/21/2017

# import the required modules
import urllib2
from bs4 import BeautifulSoup
import re
import xml.etree.ElementTree as ET
import sys
from multiprocessing.dummy import Pool as ThreadPool

# function to write to csv file
def writeListToCsv(lines,out_list,out_file):
	with open(out_file,'w') as outFile:
		for line_text in out_list:
			outFile.write(line_text)
			outFile.write("\n")

# function to get urls from csv
def get_urls_from_csv(lines,col_num):
	line_list = []
	for line in lines:
		details = line.split(',')
		kh_id = details[col_num]
		url = "https://www.aniseed.cnrs.fr/aniseed/experiment/list_insitus?organism_id=112&start_stage_id=&end_stage_id=&method_id=&filter_by_op=fate&fate_in_op=and&anat_in_op=and&gene_name="+kh_id+"&pubmed_id=&wt_only=1A"
		details.append(url)
		line_list.append(details)
	return line_list
	
# function for multithreading
def multi(line_list):
	pool = ThreadPool(4)
	out_list = pool.map(get_experiment_results,line_list)
	pool.close()
	pool.join()
	return out_list

# function to get experiment results
def get_experiment_results(line):
	exprn_url = line[-1]
	try:
		aniseed_html = urllib2.urlopen(exprn_url)
		soup = BeautifulSoup(aniseed_html,"lxml")
		info_section = soup.find("section",{"id":"informations"})
		# div tag with results number
		results_num_div = info_section.find("div",{"class":"title color_yellow"})
		results_num_text = results_num_div.text
		results_num_text = results_num_text.replace("\n","")
		matchObj = re.match(r'Experiment data \(([0-9]*) results\)',results_num_text)
		results_num = matchObj.group(1)
		temp_line = line[0:-1]
		temp_line.append(results_num)
		out_text = ','.join(temp_line)
		out_text = out_text.replace('\n','')
		return out_text	
		return results_num
	
	except Exception as e:
		# handle any other exception
		print("Error '{0}' occured. Arguments {1}.".format(e.message, e.args))
		print exprn_url
		return exprn_url

# main function
def main():
	if len(sys.argv) < 4:
		print "Usage: ",sys.argv[0]," <input file name> <output file name> <column number with KH IDs>"
		quit()
	fileName = sys.argv[1]
	out_file = sys.argv[2]
	col_num = int(sys.argv[3]) - 1
	# read in the file containing KH IDs
	with open(fileName,'r') as inFile: 
		lines = inFile.readlines()

	line_list = get_urls_from_csv(lines,col_num)
	out_list = multi(line_list)
	writeListToCsv(lines,out_list,out_file)

if __name__ == '__main__':
	main()
