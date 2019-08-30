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
          'Assembly-dna'   : [ 'DNA' , 'fasta'],
          'DNA'   : [ 'DNA' , 'contig.fasta'],
          'pep'   : [ 'pep' , 'aa.fasta'],
          'CDS'   : [ 'CDS' , 'cds.fasta'],
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

def get_files(folder,dtype):
    for file in folder.findall('file'):
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

def get_annotation_files(folder):
    for file in folder.findall('file'):
        name = file.get('label')
        url  = file.get('url')
        filename = file.get('filename')
        dtype = ""
        if re.search(r'_(prodigal|genemark)',filename):
            continue
        elif re.search(r'_contigs\.fna',filename):
            dtype = "DNA"
        elif re.search(r'_genes\.fna',filename):
            dtype = "CDS"
        elif re.search(r'_proteins\.faa',filename):
            dtype = "pep"
        else:
            print("Cannot match filename %s to a category"%(filename))

#        print("'%s' '%s'"%(filename,name))

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
        for filesfolder in topfolder.findall("folder"):
            if filesfolder.get('name') == "QC and Genome Assembly":
                if foldername == 'Assembly':
                    get_files(filesfolder,foldername+"-dna")
                for subfolder in filesfolder.findall("folder"):
                    get_files(subfolder,foldername)
            elif filesfolder.get('name') == "IMG Data":
                if foldername == 'Assembly':
                    get_annotation_files(filesfolder)
    elif foldername == "Annotation":
         for filesfolder in topfolder.find("folder"):
             if filesfolder.get('name') == "IMG Data":
                 get_annotation_files(filefolder)



with open("lib/%s.csv"%(base),"w") as jgiout:
    with open("lib/%s_jgi_download.sh"%(base),"w") as dwnload:
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
                    if ( not os.path.exists(outfile) and
                         not os.path.exists(outfile+".gz") ):
                        dwnload.write("curl -o %s '%s' -b cookies\n"
                                      %(outfile,row[-1]))
                else:
                    row.append("NO_%s_URL"%(t))
