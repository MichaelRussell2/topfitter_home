#!/bin/bash

k=0
size=100

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
    rootq rebin.cc 
    for f in mtt pt absy absytt; do
	mv ${f}_r.dat ${f}.dat
    done
    rm rebin.cc
    cd ../

    k=$((k+1))
done
