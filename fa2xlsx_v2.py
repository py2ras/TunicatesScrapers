#!/usr/bin/python

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
	worksheet = workbook.add_worksheet()
	worksheet.write(0,0,header_col0)
	worksheet.write(0,1,header_col1)
	length = len(lines)	
	row_num = 1	
	for i in range(0,length,3):
		worksheet.write(row_num,0,lines[i].replace("\n","").replace(">",""))
		worksheet.write(row_num,1,lines[i+1].replace("\n",""))
		row_num += 1	
	workbook.close()

if __name__ == '__main__':
	main()
