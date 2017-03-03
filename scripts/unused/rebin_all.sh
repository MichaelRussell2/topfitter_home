#!/bin/bash

k=0
size=$(ls -Rp results_reweighted | grep "/$" | wc -l)

rm -fr results_rebinned/
mkdir results_rebinned/

while [ $k -lt $size ]
do

    if [ $k -lt 10 ] 
    then
	var="00"$k
    elif [ $k -ge 100 ] 
    then 
	var=$k
    else
	var="0"$k
    fi

    mkdir results_rebinned/$var/
    cp results_reweighted/$var/* rebin.cc results_rebinned/$var
    cd results_rebinned/$var
    root -l -b -q rebin.cc 
    for f in mtt pt y; do
	mv ${f}_r.dat ${f}.dat
    done
    cat y.dat | awk '{print $1 "\t" $2 "\t" $3/100 "\t" $4/100}' > tmp ; mv tmp y.dat
    rm rebin.cc file.root
    cd ../../

    k=$((k+1))
done
