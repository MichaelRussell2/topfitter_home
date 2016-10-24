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
#include "lhe_read.hh"
#include <boost/spirit/include/qi.hpp>

using namespace std;
using namespace FastPartons;

namespace qi = boost::spirit::qi;
namespace ascii = boost::spirit::ascii;

void read_lhe(const string& lhefile) {

  LheEntry Entry;
  vector<LheEntry> Event;
  ifstream fin(lhefile);  
  double weight;

  if(fin){
    string line;
    int i=0;
    while(getline(fin,line)){  
      if(line == "<event>"){
	i+=1;
	if (i % 10000 == 0) cout << "At event " <<  i << endl;
	getline(fin, line);
	//event: npart, procid, weight, scale;
	vector<double> event;	  
       	qi::phrase_parse(line.begin(), line.end(),
			   *qi::double_ >> qi::eoi, ascii::space, event);
	weight = event[2];
	event.clear();
	while (true) {
	  if (line == "<mgrwt>" || line == "</event>") {
	    analyse_event(Event, weight);
	    break;
	  }
          getline(fin, line);
	  vector<double> parton; 
	  qi::phrase_parse(line.begin(), line.end(),
			   *qi::double_ >> qi::eoi, ascii::space, parton);
	  //parton: pdg, stat, moth1, moth2, col, anticol, px, py, pe, e, m;
	  if (parton.size() != 0){
	    Entry.setData(parton[0],parton[1],parton[6],parton[7],parton[8],parton[9]);
	    Event.push_back(Entry);
	    parton.clear();
	  }
	  else continue;
	}
	Event.clear();
      } 
    }
    cout << "\nAnalysed " << i << " events" << endl;
    return;
  }
  else {
    cout << "Event file not found. Exiting" << endl;
    exit(1);
  }
}

