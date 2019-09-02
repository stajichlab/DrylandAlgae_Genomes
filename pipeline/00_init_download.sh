#!/usr/bin/bash
#SBATCH -p short -N 1 -n 8
module unload miniconda2
module load miniconda3 # make sure we have python3 
module unload perl # weird problems with perl 5.22.0 on the biocluster system
module load parallel # need parallel installed to run steps in parallel

CPUS=$SLURM_CPUS_ON_NODE
if [ -z $CPUS ]; then
 CPU=1
fi

if [ ! -f scripts/init_jgi_download.sh ]; then
	echo "Need to have made scripts/init_jgi_download.sh"
	echo "cp scripts/init_jgi_download.sh.template scripts/init_jgi_download.sh"
	echo "Edit scripts/init_jgi_download.sh with USERNAME and PASSWORD for JGI"
	echo "can set the download project a different one if needed"
	exit
fi

bash scripts/init_jgi_download.sh

# may ned to add the name of the project if you change it above
#currently assumes 'Undphynobacteria'
python scripts/jgi_download.py

# this will run all the downloads
cat lib/Undphynobacteria_jgi_download.sh | parallel -j $CPU

bash scripts/fix_fasta_prefix.sh

pushd outgroups
if [ ! -f scripts/init_jgi_download.sh ]; then 
	  echo "Need to have made outgroups/scripts/init_jgi_download.sh"
	  exit
fi
bash scripts/init_jgi_download.sh
python scripts/jgi_download.py
cat cyanobacteria_jgi_download.sh | parallel -j $CPU
bash scripts/fix_fasta_prefix.sh
popd

