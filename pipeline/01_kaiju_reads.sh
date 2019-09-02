#!/bin/bash -l

#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=1
#SBATCH --mem 100gb
#SBATCH --time=02:00:00     # 2 hrs
#SBATCH --output=logs/kaiju_reads_out.%a.log
#SBATCH -p short

SAMPLES=lib/Pietrasiak_strain_names.prefix.csv
INDIR=source/JGI/fastq

CPU=$SLURM_CPUS_ON_NODE
if [ -z $CPU ]; then
	CPU=2
fi
N=${SLURM_ARRAY_TASK_ID}
module load kaiju
module load KronaTools

if [ ! $N ]; then
    N=$1
    if [ ! $N ]; then
        echo "Need an array id or cmdline val for the job"
        exit
    fi
fi
DBFOLDER=/opt/linux/centos/7.x/x86_64/pkgs/kaiju/share/DB
DB=$DBFOLDER/nr/kaiju_db_nr.fmi
NODES=$DBFOLDER/nodes.dmp
NAMES=$DBFOLDER/names.dmp
OUT=kaiju_out
mkdir -p $OUT
IFS=,
sed -n ${N}p $SAMPLES | while read PREFIX LONGNAME
do
    QUERY=$INDIR/$LONGNAME.corr.fastq.gz
    LONGNAME=$LONGNAME.reads
    echo "QUERY=$QUERY"
    if [ -f $QUERY ]; then
	if [ ! -f $OUT/$LONGNAME.out ]; then
	    kaiju -v -t $NODES -f $DB -z $CPU -a "greedy" -e 5 -s 200 -i $QUERY -o $OUT/$LONGNAME.out
	fi
	if [ ! -f $OUT/$LONGNAME.names.out ]; then
	    kaiju-addTaxonNames -u -r kingdom,phylum,genus -t $NODES -n $NAMES -i $OUT/$LONGNAME.out -o $OUT/$LONGNAME.names.out
	fi
	if [ ! -f $OUT/$LONGNAME.out.krona ]; then
	    kaiju2krona -t $NODES -n $NAMES -i $OUT/$LONGNAME.out -o $OUT/$LONGNAME.out.krona 
	fi
	if [ ! -f $OUT/$LONGNAME.out.krona.html ]; then
		ktImportText -o $OUT/$LONGNAME.out.krona.html $OUT/$LONGNAME.out.krona
	fi
	for clade in phylum family genus
	do
	    if [ ! -f $OUT/$LONGNAME.$clade.summary.tsv ]; then
		kaiju2table -t $NODES -n $NAMES -r $clade -o $OUT/$LONGNAME.$clade.summary.tsv $OUT/$LONGNAME.out
	    fi
	done
    else
	echo "Cannot find query $QUERY"
    fi
done
