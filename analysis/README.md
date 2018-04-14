# FastPartons

A simple C++ program for reading les houches event files and making basic  
1-dimensional histograms.  

Design goals:  simplicity, speed, minimal overhead

Requires the [Boost](http://www.boost.org/) C++ libraries.  

## Instructions

1. Add the path to your Boost installation to the Makefile. 
2. Book histograms, add cuts, etc. in analysis.cc  
3. Type `make` to compile, then run `./analysis <eventfile.lhe>` to plot events

