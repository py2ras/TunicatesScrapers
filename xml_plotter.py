#!/usr/bin/python

# Program to plot information from xml files
# @author: Sarthak Sharma <sarthaksharma@gatech.edu>
# Date of last change: 01/10/2018

import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
from collections import Counter

def main():
	if len(sys.argv) < 3:
		print "Usage: ./",sys.argv[0], "<xml filename>"
		quit()
	reference_fileName = sys.argv[1]							# input should be gene_expression.xml
	marker_fileName = sys.argv[2]
	marker_genes = []
	with open(marker_fileName) as mf:
		lines = mf.readlines()
	for line in lines[1:]:
		details = line.replace('"','').split(",")
		marker_genes.append(details[0])
	stage_thresh = int(sys.argv[3])
	tree = ET.parse(reference_fileName)
	all_genes = tree.findall("gene")
	common_names_list = []
	expr_regions_list = []
	for marker_gene in marker_genes:
		for gene in all_genes:
			common_name = gene.get("commonName")
			if (common_name == marker_gene):
				common_names_list.append(common_name)
				expr_territories = gene.findall("expressionTerritories")
				for expr_terr in expr_territories:
					stage_number = int(filter(str.isdigit,expr_terr.get("stage")))
					try:
						expr_region = expr_terr.text.split("-")
					except AttributeError as e:
						pass
					if (stage_number >= stage_thresh):
						#print stage_number 
						#print expr_region[0:-1]
						for x in set(expr_region[0:-1]):
							expr_regions_list.append(x)
	counts_dict = dict(Counter(expr_regions_list))
	plotter(counts_dict)
	#piePlotter(counts_dict)

def plotter(counts_dict):
	fig = plt.figure(figsize = (40.5,40.5))
	plt.barh(range(len(counts_dict)),counts_dict.values(),align='center',alpha=0.5)
	plt.yticks(range(len(counts_dict)),counts_dict.keys())
	plt.savefig("clust4.png")

def piePlotter(counts_dict):
	fig = plt.figure(figsize = (40.5,40.5))
	labels = counts_dict.keys()
	sizes = counts_dict.values()
	cmap = plt.cm.prism
	colors = cmap(np.linspace(0.,1.,len(sizes)))
	patches,texts = plt.pie(sizes,colors=colors,shadow=True,startangle=90)
	plt.legend(patches,labels,loc='lower right')
	plt.savefig("pie_clust4.png")
	
if __name__ == "__main__":
	main()
