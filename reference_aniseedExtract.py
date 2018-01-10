#!/usr/bin/python

# This script is extensively commented-
# therefore, can be used as reference in future

# Program to extract data from ANISEED-
# an online Tunicate gene expression database
# www.aniseed.cnrs.fr
# @author - Sarthak Sharma <sarthaksharma@gatech.edu>
# Date of last modification - 12/7/2017 

# import the required modules
import urllib2											# to query a website
from bs4 import BeautifulSoup									# to parse data returned from website
import re											# to extract data from strings

# specify the url
#exprn_url = "https://www.aniseed.cnrs.fr/aniseed/experiment/list_insitus?organism_id=112&start_stage_id=&end_stage_id=&method_id=&filter_by_op=fate&fate_in_op=and&anat_in_op=and&gene_name=KH.C1.1116&pubmed_id=&wt_only=1A"

# for trials, use the locally saved page - saves time
exprn_url = "file:///home/sarthak/Work/stolfi_lab/aniseed_extract/seed_page.html"

# query the website and return the html to the variable aniseed_html
aniseed_html = urllib2.urlopen(exprn_url)

# parse the HTML page and store it in Beautiful Soup format
soup = BeautifulSoup(aniseed_html,"lxml")					# return a soup object
#print soup.prettify()
#print soup.title

# to get all links on the page
#all_articles=soup.find_all("article")
#for article in all_articles:
#	print article.get("href")

#sections = soup.find_all("section")						# find_all returns a list
#for section in sections:
#	print section	
info_section = soup.find("section",{"id":"informations"})				# extract the content section from the aniseed page
#print type(content_section)							# type of object - bs4.element.tag
#print info_section

all_articles = info_section.find_all("article")
for article in all_articles:
	h2 = str(article.findAll("h2"))
	h2 = h2.replace('[','').replace(']','')
	print h2
	stage_number = re.match(r'<h2>(.*?), Stage ([0-9a-zA-Z]*) \((.*?)\)</h2>',h2,re.M|re.I)
	print stage_number.group(2)
	print stage_number.group(3)
	
	
#all_tables = info_section.find_all("table")
#for table in all_tables:
#	print table.findAll("tr")
