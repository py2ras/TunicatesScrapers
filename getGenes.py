# outline
# input - csv file with common names of genes
# output - file with regions of expression for the genes
# meta - get the accession names using common names

## Files - 
	# 'unique_gene_ids_txt' -> contains geneIDs with their unique names
	# 'url_list.txt' -> contains urls to get gene dicts
	# 'uniq_names.txt' -> contains the list of unique names of genes without their GeneIDs

import sys

def main():
	if len(sys.argv) < 2:
		print("Usage: python ", sys.argv[0], " <file name>")
		quit()

	fileName = sys.argv[1]
	with open(fileName,'rb') as inFile:
		lines = inFile.readlines()

	# out_uniq(lines)
	# out_urls(lines)
	expression_urls(lines)


# here input is 'unique_gene_ids.txt'	
def out_uniq(lines):
	with open('uniq_names.txt','a') as outFile:
		for line in lines[1:]:
			geneId = line.split(',')[1]
			outFile.write(geneId+"\n")

# here input is 'uniq_names.txt'
def out_urls(lines):
	print "urls"
	with open('url_list.txt','a') as outFile:
		for line in lines:
			gene = line.lower().strip('\n')
			url = "dev.aniseed.cnrs.fr/api/all_territories_by_gene:?gene="+gene+"&organism_id=112"
			outFile.write(url+"\n")
	print "done"

# here the input is 'unique_gene_ids.txt'
def expression_urls(lines):
	with open('exprsn_url_list_4.txt','w') as outFile:
		for line in lines[1:]:
			details = line.split(',')
			geneId = details[0]
			geneId = geneId[7:]
			expr_url = "https://www.aniseed.cnrs.fr/aniseed/experiment/list_insitus?organism_id=112&start_stage_id=&end_stage_id=&method_id=&filter_by_op=fate&fate_in_op=and&anat_in_op=and&gene_name="+geneId+"&pubmed_id=&wt_only=1A"
			print geneId
			outFile.write(details[0]+","+details[1]+","+expr_url+"\n")
			# outFile.write()	

if __name__ == '__main__':
	main()

# regex to select everything before the first '/'