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
    elif [ $k -le 100 ] 
    then 
	var=$k
    else
	var="0"$k
    fi

    mkdir results_rebinned/$var/
    cp results_reweighted/$var/* rebin.cc results_rebinned/$var
    cd results_rebinned/$var
    root -l -b -q rebin.cc 
    for f in mtt pt absy; do
	mv ${f}_r.dat ${f}.dat
    done
    rm rebin.cc file.root
    cd ../../

    k=$((k+1))
done
