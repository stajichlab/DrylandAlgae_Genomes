# Download and processes JGI Cyano genomes for Project with NMSU

Author - Jason Stajich, jason.stajich[AT]ucr.edu

# To download from JGI

```bash
$ cp scripts/init_jgi_download.sh.template scripts/init_jgi_download.sh
# edit scripts/init_jgi_download.sh with your JGI email and password
# then run the following, this will establish the lib folder and XML download from JGI
$ bash scripts/init_jgi_download.sh
# this script will run by default on the XML downloaded from JGI
$ python scripts/jgi_download.py
# and will create a file in  lib/Undphynobacteria_jgi_download.sh
# which has a set of commands to download the data
# I do this in parallel with the parallel command
$ cat lib/Undphynobacteria_jgi_download.sh | parallel -j 8
# but you can also just run
$ bash lib/Undphynobacteria_jgi_download.sh
```

Now you have donwloaded the raw FASTQ corrected files, assembly, and IMG annotation from JGI.
We can now proceed to phylogeny or other analyses


## Phylogenomic analyses
1. Resolve Cyanobacteria tree of life
2. Gene content comparisons

# Compare these strains to metagenomes from desert environments
