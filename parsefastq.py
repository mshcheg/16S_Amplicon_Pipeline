#!/bin/python


'''
    This script splits a fastq file containing sequence data for many barcoded samples into individual files by sample. 
    
    To run this script a file linking sample id's to sequencing barcode id's must be provided along with the input fastq file.

    Author: Mariya Shcheglovitova
    Email: m.shcheglovitova@gmail.com
    License: Creative Commons Attribution
'''

import csv
import os
import argparse

#Parse commandline arguments 
parser = argparse.ArgumentParser(description='Seperate sequences in fastq file into individual files by sample.')
parser.add_argument('-s', '--sample', action="store", type=str, metavar="samplesfile", required=True, nargs=1, help='a sample file mapping barcodes to sample ids')
parser.add_argument('-r1', '--read1', action="store", metavar='read1file', type=str, required=True, nargs=1, help='read one fastq file')
parser.add_argument('-r2', '--read2', action="store", metavar='read2file', type=str, required=True, nargs=1, help='read two fastq file')
parser.add_argument('-o', '--outdirectory', action="store", metavar='outdirectory', type=str, required=True, nargs=1, help='directory for writing output')
parser.add_argument('-p', '--primer', action="store", metavar='primername', type=str, required=False, nargs=1, help='optional argument to add primer name to output files')

args = parser.parse_args()

if not os.path.exists(args.outdirectory[0]):
        	os.makedirs(args.outdirectory[0])

#Create a dictionary linking sample names to barcode names.
SampletoBarcode = {}

i=0
j=0
with open(args.sample[0], 'rb') as csvfile:
    LookUpReader = csv.reader(csvfile, delimiter='\t') 
    for row in LookUpReader:
        if i == 0:
            SampleIndex = row.index('SampleID')
            BarcodeIndex = row.index('BarcodeID')
            i = 1
        else:
            sample = "_".join(row[SampleIndex].split())
            barcode = row[BarcodeIndex]
            if sample == "Neg":
                sample = sample+str(j)
                SampletoBarcode[barcode] = sample
                j+=1
            else:
                sample = sample
                SampletoBarcode[barcode] = sample


with open(args.read1[0], 'r') as R1file:
	with open(args.read2[0], 'r') as R2file:
		while 1: #initiate infinite loop
    			#read 4 lines of the fasta file
    			SequenceHeader1= R1file.readline()
    			Sequence1= R1file.readline()
    			QualityHeader1= R1file.readline()
    			Quality1= R1file.readline()
			
			if SequenceHeader1 == '': #exit loop when end of file is reached
        			break
			
			barcode = SequenceHeader1.split()[1].split(":")[3] 			
				
			SequenceHeader2= R2file.readline()
    			Sequence2= R2file.readline()
    			QualityHeader2= R2file.readline()
    			Quality2= R2file.readline()
			
			try: 
				Outfile1 = "%s/%s_%s_%s_R1.fastq" %(args.outdirectory[0], SampletoBarcode[barcode], barcode, args.primer[0])
				Outfile2 = "%s/%s_%s_%s_R2.fastq" %(args.outdirectory[0], SampletoBarcode[barcode], barcode, args.primer[0])    			
			except TypeError:
				Outfile1 = "%s/%s_%s_R1.fastq" %(args.outdirectory[0], SampletoBarcode[barcode], barcode)
				Outfile2 = "%s/%s_%s_R2.fastq" %(args.outdirectory[0], SampletoBarcode[barcode], barcode)    

			with open(Outfile2, 'a') as out2:    			
				out2.write('%s%s%s%s' %(SequenceHeader2, Sequence2, QualityHeader2, Quality2))	
    			with open(Outfile1, 'a') as out1:
				out1.write('%s%s%s%s' %(SequenceHeader1, Sequence1, QualityHeader1, Quality1))

with open("%s/stability.files" %args.outdirectory[0],'w') as log:		
	myfiles = os.listdir(args.outdirectory[0])
 	uniquefiles = set(["_".join(x.split("_")[0:len(x.split("_"))-1]) for x in myfiles])
	for f in uniquefiles:
		if f not in ['stability.files', '']:
			sample = f.split("_")[0]
			R1 = "%s_R1.fastq" %f
			R2 = "%s_R2.fastq" %f		
			log.write("%s\t%s\t%s\n" %(sample, R1, R2))
		else:
			continue	
