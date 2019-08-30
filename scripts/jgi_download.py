#!/usr/bin/env python3

import os, sys, logging, csv, re

import xml.etree.ElementTree as ET
DEBUG=1

skipme='lib/skip_data_jgi.csv'


skip_data = {}
if os.path.exists(skipme):
    with open(skipme,'r') as skips:
        skipread = csv.reader(skips,delimiter=",")
        skipheader = next(skipread)
        for row in skipread:
            if len(row):
                skip_data[row[0]] = 1

base    = 'Undphynobacteria' # default for Nicole's JGI project
if len(sys.argv) > 1: # if a command line argument is provided
    base    = sys.argv[1]
xmlfile  = "lib/%s.xml" % (base)
outdir="source/JGI"

mapext = {'Sequence'   : [ 'fastq', 'corr.fastq.gz'],
          'Assembly'  : [ 'info', 'coverage.txt' ],
          'Assembly-dna'   : [ 'DNA' , 'fasta.gz'],
          'Alignment'  : [ 'SAM', 'sam.gz' ],
      }

# make the top level folder for storing the data
if not os.path.exists(outdir):
    os.mkdir(outdir)
# make the folders for storing the data - process mapext dictionary
for t in mapext.values():
    if not os.path.exists(os.path.join(outdir,t[0])):
        os.mkdir(os.path.join(outdir,t[0]))

if not os.path.exists(xmlfile):
    print("expecting %s - did you run scripts/init_jgi_download.sh?"%(xmlfile))
    exit()

hosturl='https://genome.jgi.doe.gov'
species = {}
tree = ET.parse(xmlfile)
root = tree.getroot()

def get_qc_reads_asssembly(folderroot,dtype):
    for asmfolder in folderroot.findall("folder"):
        for file in asmfolder.findall('file'):
            name = file.get('label')
            url  = file.get('url')
            if name not in species:
                species[name] = {dtype: [url,name]}
            elif dtype not in species[name]:
                species[name][dtype] = [url,name]
            else:
                print("warning - updating %s %s with url (%s) when it was previously %s"
                      % (name,dtype,url,species[name][dtype][0]))
                species[name][dtype] = [url, name]

# main code
for topfolder in root.findall('folder'):
    foldername = topfolder.get('name')
    if (  foldername == 'Sequence' or foldername == 'Assembly' or
          foldername == 'Alignment'):
        print("in %s"%(foldername))

        for filesfolder in topfolder.findall("folder"):
            if filesfolder.get('name') == "QC and Genome Assembly":
                if foldername == 'Assembly':
                    for fi in filesfolder.findall("file"):

                        print(fi.get('label'),fi.get('filename'),fi.get('url'))
                get_qc_reads_asssembly(filesfolder,foldername)



with open("lib/%s.csv"%(base),"w") as jgiout:
    with open("lib/%s_jgi_download.test.sh"%(base),"w") as dwnload:
        jgicsv = csv.writer(jgiout,delimiter=",",lineterminator="\n")
        jgicsv.writerow(['Label','read_URL','asm_URL'])
        for sp in sorted(species.keys()):
            row = ['',sp]
            for t in mapext.keys():
                if t in species[sp]:
                    if len(row[0]) == 0:
                        row[0] = species[sp][t][1]
                    row.append(hosturl + species[sp][t][0])
                    outfile="%s.%s"%(os.path.join(outdir,mapext[t][0],
                                                  row[0]),mapext[t][1])
                    if not os.path.exists(outfile):
                        dwnload.write("curl -o %s '%s' -b cookies\n"
                                      %(outfile,row[-1]))
                else:
                    row.append("NO_%s_URL"%(t))
