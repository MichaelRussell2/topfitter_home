#include <iostream>
#include <sstream>
#include <fstream>
#include <valarray>
#include <cmath>
#include <cassert>
#include <vector>
#include <tuple>
#include <algorithm>
#include "analysis.hh" 
#include "histo.hh"
#include "lhe_read.hh"

using namespace std;
using namespace FastPartons;

//initialise weights
double sumWeights = 0.;

//book histograms here 
Histo Histo1(0,2000,50);
Histo Histo2(0,1000,10);
Histo Histo3(-2.5,2.5,0.1);

//simple main function
int main(int argc, const char** argv){

  if (argc != 2) {
    cout << "Give input event file as argument" << endl;
    return 0;
  }  
  const string infile = argv[1];

  read_lhe(infile); 

  //write out histograms to file 
  Histo1.write("mtt.dat");
  Histo2.write("pt.dat");
  Histo3.write("yt.dat"); 
  cout << "Total cross-sec : " << sumWeights << " pb " << endl;
  return 0;
}

void analyse_event(vector<FastPartons::LheEntry> Event, double weight) {

  sumWeights += weight;
  
  //kinematic variables to plot
  double pt, mtt, yt;
  Particle t;
  Particle tbar;

  //Loop over particles in event
  for(int i=0; i<Event.size(); i++){

    LheEntry Entry = Event.at(i);

    //only look at final state particles
    //if (Entry.stat != 1) continue;

    if(Entry.pdg==6){     
      t.setMomentum(Entry.Px(),Entry.Py(),Entry.Pz(),Entry.E());
    }
    
    else if(Entry.pdg==-6){     
      tbar.setMomentum(Entry.Px(),Entry.Py(),Entry.Pz(),Entry.E());
    }  
   
    mtt = (t+tbar).Mass();
    pt  = t.pT();
    yt  = t.y();
  }
  Histo1.fill(mtt,weight);
  Histo2.fill(pt,weight);
  Histo3.fill(yt,weight);
  return; 
}
