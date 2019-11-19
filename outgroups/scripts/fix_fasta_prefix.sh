#!/usr/bin/bash
#SBATCH -p short --out logs/rename_fasta.log

pushd source/JGI/pep
for file in *.aa.fasta
do
	p=$(basename $file .aa.fasta)
	perl -i -p -e "s/^>/>$p|/" $file 
done
popd

pushd source/JGI/CDS
for file in *.cds.fasta
do
	p=$(basename $file .cds.fasta)
	perl -i -p -e "s/^>/>$p|/" $file
done
popd
