#!/usr/bin/env python3

import csv, re, sys, os
import xml.etree.ElementTree as ET
from Bio import Entrez


def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

Entrez.email = 'jason.stajich@ucr.edu'
insamples = "lib/MRA_Table1.tsv"
outsamples="lib/MRA_Table1_edit.tsv"

if len(sys.argv) > 1:
    insamples = sys.argv[1]

if len(sys.argv) > 2:
    outsamples = sys.argv[2]

seen = {}
if os.path.exists(outsamples):
    with open(outsamples,"rU") as preprocess:
        incsv = csv.reader(preprocess,delimiter=",")
        h = next(incsv)
        for row in incsv:
            seen[row[0]] = row

with open(insamples,"rU") as infh, open(outsamples,"w") as outfh:
    outcsv    = csv.writer(outfh,delimiter="\t")
    # Genus	Species	Strain ID	NCBI BioProject ID	NCBI SRA Run	JGI IMG ID	# of Reads	N contigs	N50	Habitat	Location
    outcsv.writerow(['GENUS','SPECIES','STRAIN','BioProject','SRA Project','SRA Run','IMG_ID','N_Reads','N_Contigs','N50',
    'Habitat','Location'])

    samplescsv = csv.reader(infh,delimiter="\t")
    headerrow = next(samplescsv)
    for row in samplescsv:
        outrow = row

        BIOPROJECTID = row[3]
        print(row)
        SRARUN = []
        NREADS = 0
        NBASES = 0
        if BIOPROJECTID:
            SRP = row[4]
            handle = Entrez.esearch(db="sra",retmax=10,term=SRP)
            record = Entrez.read(handle)
            for id in record["IdList"]:
                SRP = id
            handle.close()

            #SRP=row[4]
            handle = Entrez.efetch(db="sra",id = SRP)
            tree = ET.parse(handle)
            root = tree.getroot()
            for runs in root.iter('RUN_SET'):
                    for run in runs.iter('RUN'):
                        SRARUN.append(run.attrib['accession'])
                        #indent(run)
                        #print(ET.tostring(run))
                    for dbs in runs.iter('Databases'):
                        #indent(dbs)
                        #print(ET.tostring(dbs))
                        for stats in dbs.iter('Statistics'):
                            for datrow in stats.iter('Rows'):
                                NREADS += int(datrow.attrib['count'])
                    #for bases in runs.iter('Bases'):
                    #    NBASES += bases.attrib['count']
            #indent(root)
            #print(ET.tostring(root))
        outrow[5] = ",".join(SRARUN)
        outrow[7] = NREADS
        outcsv.writerow(outrow)
