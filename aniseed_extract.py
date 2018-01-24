#!/usr/bin/python

# Program to extract data from ANISEED-
# an online Tunicate gene expression database
# www.aniseed.cnrs.fr
# @author - Sarthak Sharma <sarthaksharma@gatech.edu>
# Date of last modification - 12/7/2017 

# import the required modules
import urllib2											# to query a website
from bs4 import BeautifulSoup									# to parse data returned from website
import re											# to extract data from strings
import xml.etree.ElementTree as ET								# to write output to xml file
import sys											# to take command-line inputs
# specify the url
#exprn_url = "https://www.aniseed.cnrs.fr/aniseed/experiment/list_insitus?organism_id=112&start_stage_id=&end_stage_id=&method_id=&filter_by_op=fate&fate_in_op=and&anat_in_op=and&gene_name=KH.C1.1116&pubmed_id=&wt_only=1A"

# for trials, use the locally saved page - saves time
#exprn_url = "file:///home/sarthak/Work/stolfi_lab/aniseed_extract/seed_page.html"

def writeXML(out_dict,fileName):
	root = ET.Element("genesExpressionTerritories")
	for gene_name,mixed_list in out_dict.iteritems():			# Each key in the dictionary is gene_name
		gene_detail_list = mixed_list[0]
		common_name = gene_detail_list[1]
		exprn_url = gene_detail_list[2]
		stages_dict= mixed_list[1]
		gene = ET.SubElement(root,"gene")
		gene.set("name",gene_name)
		gene.set("commonName",common_name)
		gene.set("url",exprn_url)					# not needed for now - uncomment, if needed in future
		for stage in sorted(stages_dict):
			exprn_terr = stages_dict[stage]
			expr = ET.SubElement(gene,"expressionTerritories")
			expr.set("stage",stage)
			expr.text = exprn_terr
	tree = ET.ElementTree(root)
	#tree.write("C_robusta_gene_expressions.xml")
	matchObj = re.match('([0-9]*)_.*',fileName,re.M|re.I)
	end_number = matchObj.group(1)
	outFileName = str(int(end_number)-500)+"_"+end_number+".xml"
	tree.write(outFileName)
	#tree.write("1500_2000.xml")

def get_exprn_urls(lines):
	genes_details = []
	for line in lines[1:]:
		details = line.split(',')
		gene_name = details[0]
		gene_name = gene_name[7:]
		common_name = details[1]
		exprn_url = "https://www.aniseed.cnrs.fr/aniseed/experiment/list_insitus?organism_id=112&start_stage_id=&end_stage_id=&method_id=&filter_by_op=fate&fate_in_op=and&anat_in_op=and&gene_name="+gene_name+"&pubmed_id=&wt_only=1A"
		genes_details.append([gene_name,common_name,exprn_url])
	return genes_details

def get_table_details(genes_details):
	out_dict = {}											# key=GeneName(gene_name), value=MixedList(mixed_list)
	num_gene = 0
	for gene_detail_list in genes_details:
		mixed_list = []										# will contain 2 lists - gene_detail_list and stages_list
		gene_name = gene_detail_list[0]
		exprn_url = gene_detail_list[2]
		print "Working on: ",num_gene,"-",gene_name," ..."
		num_gene += 1
		# gene_detail_list = [gene_name,common_name,exprn_url]
		mixed_list.append(gene_detail_list)
		#stages_list = []
		aniseed_html = urllib2.urlopen(exprn_url)
		soup = BeautifulSoup(aniseed_html,"lxml")						# return a soup object

		# required information is in the information section of the HTML		
		info_section = soup.find("section",{"id":"informations"})				# extract the content section from the aniseed page

		# each article contains single expression region info	
		all_articles = info_section.find_all("article")

		stages_dict = {}
		# every information that needs to be extracted should be extracted in the following loop
		for article in all_articles:
			# h2 have stage details
			h2 = str(article.findAll("h2"))
			h2 = h2.replace('[','').replace(']','')
			matchObj = re.match(r'<h2>(.*?), Stage ([0-9a-zA-Z]*) \((.*?)\)</h2>',h2,re.M|re.I)
			stage_number = matchObj.group(2)
			stage_name = matchObj.group(3)
			all_tables = article.find_all("table")
			for table in all_tables:
				all_row_data = table.findAll("td")						# the main table data is stored in td
				exprn_terr = all_row_data[3].string.encode("utf-8")				# expression territory is the 4th element; changing the encoding to utf-8 for better printing to file
				exprn_terr = exprn_terr.replace("\n","").replace(" ","")
				if stage_number in stages_dict:
					stages_dict[stage_number] += exprn_terr
				else:
					stages_dict[stage_number] = exprn_terr

		mixed_list.append(stages_dict)
		out_dict[gene_name] = mixed_list
	return out_dict

def main():
	if len(sys.argv) < 2:
		print "Usage: ./",sys.argv[0]," <file name>"
		quit()
	# input should be "unique_gene_ids.txt"
	fileName = sys.argv[1]
	# read in the file containing gene names 
	with open(fileName,'rb') as inFile:
		lines = inFile.readlines()

	# construct the URLs from gene names
	genes_details =	get_exprn_urls(lines)
	# get the expression details using the above details
	out_dict = get_table_details(genes_details)
	writeXML(out_dict,fileName)

if __name__ == '__main__':
	main()
