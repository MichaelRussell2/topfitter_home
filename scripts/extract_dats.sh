#!/bin/bash

## script to extract data histograms from ME topdrawer file
## using some command line magic
## TODO: pythonise this at some point
## Usage: ./extract_dats <histo_name> (in double quotes!) <name_of_outfile>
## Run with no arguments to see available histos

## function to count histograms contained in file
function find_histos() {
    grep 'TITLE TOP' $1 | cut -d '"' -f2
}

infile=plots.top
histo=${1}
outfile=${2}

if [ ! -e $infile ]
then
    echo "Input file "$infile" not found"
    exit 1
fi

if [ $# -eq 0 ]
then
    echo "Available histograms in this file are:"
    find_histos $infile
    exit 0
elif [[ ! $# -eq 0 && ! $# -eq 2 ]]
then
    echo "Wrong number of arguments. Exiting"
    exit 2
fi

x1=$(grep -n $histo $infile | sed -e 's/:.*//g' )

if [ $x1 ] 
then
    sed -n "$((x1+7)),$ p" $infile > file.tmp 
    x2=$(grep -m1 -n HISTO file.tmp | sed -e 's/:.*//g'  ) 
    head -n$((x2-1)) file.tmp  > $outfile
    rm file.tmp
else
    echo " Histogram '"$histo"' doesn't exist in this file"
    echo " Available histograms in this file are:"
    echo
    find_histos $infile
    echo
    exit 3
fi
