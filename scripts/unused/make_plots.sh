#!/bin/bash

k=0
size=$(ls -A plots/ | wc -l)

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

    ./extract_dats.sh plots/plots$var.top 'pt(t11)' results/$var/pt.dat
    ./extract_dats.sh plots/plots$var.top 'y(t11)' results/$var/y.dat
    ./extract_dats.sh plots/plots$var.top 'X1(t11)' results/$var/absy.dat
    ./extract_dats.sh plots/plots$var.top 'm(t11,t21)' results/$var/mtt.dat
    cp param_space/$var/used_params results/$var

    k=$((k+1))
done
