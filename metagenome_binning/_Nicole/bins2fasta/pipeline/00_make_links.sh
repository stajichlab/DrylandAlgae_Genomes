#!/usr/bin/bash
module load hmmer/3
mkdir -p input genomes
AUTOMETAFOLDER=../..
GENOMEDIR=../../../../source/JGI/DNA/from_IMG_tar
pushd input
for n in $(ls $AUTOMETAFOLDER/20181*/ML*.tab); do 
	dir=`basename $(dirname $n)`
	if [ ! -f $dir.ML_recruitment.tab ]; then
		ln -s $n $dir.ML_recruitment.tab
	fi
	done
popd 

pushd genomes
for n in $(ls $GENOMEDIR/*.fasta | grep -v contig)
do
	if [ ! -f $(basename $n) ]; then
		ln -s $n .
	fi
	if [ -f $n.ssi ]; then
		ln -s $n.ssi .
	else
		esl-sfetch --index $(basename $n)
	fi
done
popd
