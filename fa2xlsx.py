#!/usr/bin/python

# Program to convert fasta to xlsx format
# This limits the number of rows in each sheet to 50
# Requires xlsxwriter library
# Outputs a single workbook
# @author: Sarthak Sharma <sarthaksharma@gatech.edu>
# Date of last change: 01/10/2018

import sys
import xlsxwriter

def main():
	fileName = sys.argv[1]
	outFile = fileName[:-3] + "+test.xlsx"
	header_col0 = "SequenceName"
	header_col1 = "Sequence"
	with open(fileName) as inFile:
		lines = inFile.readlines()
	workbook = xlsxwriter.Workbook(outFile)
	
	worksheet = workbook.add_worksheet("1")
	worksheet.write(0,0,header_col0)
	worksheet.write(0,1,header_col1)
	length = len(lines)	
	row_num = 1	
	worksheet_num=1
	for i in range(0,length,3):
		worksheet.write(row_num,0,lines[i].replace("\n","").replace(">",""))
		worksheet.write(row_num,1,lines[i+1].replace("\n",""))
		row_num += 1	
		if row_num >49: 
			worksheet_num += 1
			worksheet = workbook.add_worksheet(str(worksheet_num))
			worksheet.write(0,0,header_col0)
			worksheet.write(0,1,header_col1)
			row_num = 1
	workbook.close()

if __name__ == '__main__':
	main()
