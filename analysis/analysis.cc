#include <analysis.hh> 
#include <histo.hh>
#include <lhe_read.hh>

using namespace std;
using namespace FastPartons;

//initialise weights
double sumWeights = 0.;

//book histograms here 
Histo h_mtt(0,2000,50);
Histo h_pt(0,1000,10);
Histo h_yt(-2.5,2.5,0.1);

Histo2d h_mtt_pt(0,2000,50,0,1000,10);
double wgts;

//simple main function
int main(int argc, const char** argv){

  if (argc != 2) {
    cout << "Give input event file as argument" << endl;
    return 0;
  }  
  const string infile = argv[1];
  read_lhe(infile); 

  //write out histograms to file
  h_pt.addOverflow();
  
  h_mtt.write("mtt.dat");

  h_pt.sumw2();
  h_pt.write("pt.dat");
  h_yt.write("yt.dat");
  h_mtt_pt.write("mtt_pt.dat");
  cout << "Total cross-sec : " << sumWeights << " pb " << endl;
  cout << wgts << endl;
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

  h_mtt.fill(mtt,weight);
  h_pt.fill(pt,weight);
  h_yt.fill(yt,weight);

  h_mtt_pt.fill(mtt,pt,weight);
  return; 
}
