#!/usr/bin/bash
mkdir -p cyano_bins
module load hmmer/3
for d in input/*.tab; 
do 
	b=$(basename $d .ML_recruitment.tab); 
	asm=$(echo $b | perl -p -e 's/_FD//').fasta
	grep Cyanobacteria $d | cut -f1 | esl-sfetch -f assemblies/$asm - > cyano_bins/$b.Cyano_bin.fasta; 
done
