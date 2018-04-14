#ifndef ANALYSIS_HH
#define ANALYSIS_HH

#include <iostream>
#include <sstream>
#include <fstream>
#include <valarray>
#include <cmath>
#include <cassert>
#include <vector>
#include <tuple>
#include <algorithm>

using namespace std;
namespace FastPartons {

#define SkipEvent {return;}
  
  class Particle {
    
  public:
    
    int Pdg;
    int Stat;
    double Px;
    double Py;
    double Pz;
    double E;
    
    double pT(){return(sqrt(Px*Px+Py*Py));}
    double Mass(){return(sqrt(E*E-Px*Px-Py*Py-Pz*Pz));}
    double ET(){return(sqrt(Mass()*Mass()+pT()*pT()));}
    double y(){return(0.5*(log((E+Pz)/(E-Pz))));}

    double eta(){
      if (Px == 0 && Py == 0) return 1000.;
      if (Pz == 0) return 0.;
      
      double theta = atan(pT()/Pz);
      if (theta < 0) theta += pi;
      return -log(tan(theta/2));
    }

    double phi(){
      if (Px == 0 && Py == 0) return 0.;
      double _phi = atan2(Py,Px);
      if (_phi < 0.0) _phi += 2*pi;
      if (_phi >= 2*pi) _phi -= 2*pi; 
      return _phi;
    }
    
    Particle setMomentum(double& Px, double& Py, double& Pz, double& E){
      this->Px = Px;
      this->Py = Py;
      this->Pz = Pz;
      this->E = E;
      return *this;
    }
    
    //overload operators for Particle class
    Particle operator+(const Particle& other) const;
    Particle operator-(const Particle& other) const;

  private:
    double pi = 4*atan(1); 
        
  };

  inline bool SortByPt(Particle p1, Particle p2){
    return p1.pT() > p2.pT();
  }

  //constrain between [-pi, pi]
  inline double deltaPhi(Particle p1, Particle p2){
    double pi = 4*atan(1); 
    double dPhi = p1.phi()-p2.phi();
    if (dPhi < pi) dPhi += 2*pi;
    if (dPhi > pi) dPhi -= 2*pi;
    return dPhi;
  }
  
  inline double deltaR(Particle p1, Particle p2){
    return sqrt(pow(p1.eta()-p2.eta(),2)+pow(deltaPhi(p1,p2),2));
  }

  inline Particle Particle::operator+(const Particle& other) const {
    Particle tmp = *this;
    tmp.Px = this->Px + other.Px;
    tmp.Py = this->Py + other.Py;
    tmp.Pz = this->Pz + other.Pz;
    tmp.E = this->E + other.E;
    return tmp;   
  }
  
  inline Particle Particle::operator-(const Particle& other) const {
    Particle tmp = *this;
    tmp.Px = this->Px - other.Px;
    tmp.Py = this->Py - other.Py;
    tmp.Pz = this->Pz - other.Pz;
    tmp.E = this->E - other.E;
    return tmp;   
  }

  
  
  class LheEntry {
    
  public:
    
    double px;
    double py;
    double pz;
    double e;
    
    double pdg;
    double stat;
    double col;
    double anticol;
    double moth1;
    double moth2;

    double& Px(){return px;} 
    double& Py(){return py;} 
    double& Pz(){return pz;} 
    double& E(){return e;} 
    
    LheEntry setData(double& pdg, double& stat,  double& px, double& py, double& pz, double& e){
      this->pdg = pdg;
      this->stat = stat;
      this->px = px;
      this->py = py;
      this->pz = pz;
      this->e = e;
      return *this;

    }
  };
  
}

//function prototypes
void analyse_event(vector<FastPartons::LheEntry> Event, double weight);

#endif
