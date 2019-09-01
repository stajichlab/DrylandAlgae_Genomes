#!/usr/bin/bash
module unload miniconda2
module load miniconda3

mkdir -p source/JGI
scripts/jgi_download.py blastocladiomycota
scripts/jgi_download.py chytridiomycota

./scripts/rename_JGI_shortfiles.py lib/blastocladiomycota_names.tab | parallel -j 4
./scripts/rename_JGI_shortfiles.py lib/chytridiomycota_names.tab | parallel -j 4
