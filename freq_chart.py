# Program to plot frequency of territorial expression
# in clusters

# Input - cluster.x.cxv
# output - bar chart

import sys

def main():
	if len(sys.argv) < 2:
		print("Usage: python ", sys.argv[0], " <file name>")
		quit()

	cluster_at_list = []
	count = 0
	fileName = sys.argv[1]
	with open(fileName,'rb') as inFile:
		lines = inFile.readlines()
	for line in lines:
		line = line.split(',')
		gene = line[6].lower().strip('\n').replace('"','').strip()
		# print gene
		# print len(line)
		try:
			with open("all_csvs/"+gene + ".csv") as f:
				terr_st_lines = f.readlines()
				# print terr_st_lines[0]
				# print terr_st_lines[1:]
				# count = count + 1
				print gene
		except Exception as e:
			with open('log.txt','a') as log:
				log.write(gene+"not found!\n")
		# if count > 10:
		# 	break
		# print count

# def get_enrichment(lines):


if __name__ == '__main__':
	main()