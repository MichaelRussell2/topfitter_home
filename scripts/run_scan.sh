#!/bin/bash

rm -fr plots/ results/ samples/outputs/ samples/Events/*
mkdir plots/ results/ samples/outputs/

main=${PWD}
k=0
size=$(ls -Rp param_space/ | grep "/$" | wc -l)

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
 
    rm -fr results/$var/
    mkdir results/$var/
    cp param_space/$var/used_params results/$var/

    c1=`awk ' FNR ==1 {print $2}'  param_space/$var/used_params `
    c2=`awk ' FNR ==2 {print $2}'  param_space/$var/used_params `
    c3=`awk ' FNR ==3 {print $2}'  param_space/$var/used_params `
    c4=`awk ' FNR ==4 {print $2}'  param_space/$var/used_params `
    c5=`awk ' FNR ==5 {print $2}'  param_space/$var/used_params `
    c6=`awk ' FNR ==6 {print $2}'  param_space/$var/used_params `
   
    cp param_card_sm.dat param_card.dat
    sed -i "s/0e-08 # CG /${c1}e-08 # CG /" param_card.dat
    sed -i "s/0e-08 # ReCuG33/${c2}e-08 # ReCuG33/" param_card.dat
    sed -i "s/0e-08 # C1qq1331 /${c3}e-08 # C1qq1331 /" param_card.dat
    sed -i "s/0e-08 # C8qu3311/${c4}e-08 # C8qu3311/" param_card.dat
    sed -i "s/0e-08 # C3qq1331/${c5}e-08 # C3qq1331/" param_card.dat
    sed -i "s/0e-08 # C8ud3311/${c6}e-08 # C8ud3311/" param_card.dat
       
    mv param_card.dat samples/Cards/
    cd samples/
    ./bin/generate_events -f --laststep=parton  > outputs/output$var
    
    gunzip Events/run_01/unweighted_events.lhe.gz
    mv Events/run_01/unweighted_events.lhe MadAnalysis/
    
    cd MadAnalysis/
    rm -f plots.top 
    ./plot_events
    rm -f unweighted_events.lhe*
    
    mv plots.top $main/plots/plots$var.top
    cd $main
    rm -fr samples/Events/*
    
    k=$((k+1))
    
done
