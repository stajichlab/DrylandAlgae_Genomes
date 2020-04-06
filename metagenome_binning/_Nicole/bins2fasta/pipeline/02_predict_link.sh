#!/usr/bin/bash
#SBATCH -p short -N 1 -n 8 --mem 8gb --out cyano_prodigal.log
module load prodigal
module unload perl
module load parallel
INDIR=cyano_bins
pushd $INDIR
#parallel -j 8 prodigal -i {} -a {.}.faa -o {.}.prodigal.out ::: $(ls *.fasta)
for faa in $(ls *.faa)
do
	PREF=$(basename $faa .Cyano_bin.faa)
	perl -i -p -e "s/^>scaf/>$PREF|scaf/" $faa
done

popd
mkdir -p proteins
IFS=,
cat Pietrasiak_strain_names.prefix.csv | while read PREFIX FULL
do
	ln -s ../cyano_bins/$PREFIX.Cyano_bin.faa proteins/$FULL.aa.fasta
done
