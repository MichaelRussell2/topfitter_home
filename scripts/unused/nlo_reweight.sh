#!/bin/bash

k=0 
size=` ls -Rp results/ | grep "/$" | wc -l`

rm -fr results_reweighted/
mkdir results_reweighted/

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

    rm -fr results_reweighted/$var/
    mkdir results_reweighted/$var/

    paste results/$var/mij.dat kfactors/mij.dat | awk '{print $1 " " $2*$5 " " $2*$7 }' > results_reweighted/$var/mij.dat 
    paste results/$var/pt.dat kfactors/pt.dat | awk '{print $1 " " $2*$5 " " $2*$7 }' > results_reweighted/$var/pt.dat 
    paste results/$var/absyij.dat kfactors/absyij.dat | awk '{print $1 " " $2*$5 " " $2*$7 }' > results_reweighted/$var/absyij.dat 

    cp results/$var/used_params results_reweighted/$var/used_params
   
    k=$((k+1))
done
