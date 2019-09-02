#!/usr/bin/bash

pushd kaiju_out
echo "Contig Krona plots" > index.md
echo "==================" >> index.md
ls *.contig.out.krona.html | perl -p -e 's/(\S+)/* [$1]($1)/'  >> index.md
echo "" >> index.md
echo "Reads Krona plots" >> index.md
echo "==================" >> index.md
ls *.reads.out.krona.html | perl -p -e 's/(\S+)/* [$1]($1)/'  >> index.md
