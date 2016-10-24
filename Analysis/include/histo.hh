#ifndef HISTO_HH
#define HISTO_HH

#include <iostream>
#include <cmath>

using namespace std;
namespace FastPartons{
  
  class Histo {
  public:
    
    //    Histo();
    //    ~Histo();
    
    //constructor
    Histo(double xmin, double xmax, double binWidth);

    
    void book(double xmin, double xmax, double binWidth);
    void fill(double entry);
    void fill(double entry, double weight);
    void write(const char *outfile);
    int bins();                    
    int count(int bin);         
    int getunderflowcount();// @TODO: define this     
    int getoverflowcount(); // @TODO: define this     
    double lowerBound(int bin);
    double upperBound(int bin);
   
    
    //virtual ~Histo();
    
  private:
    double min;
    double max;
    double binWidth;
    int binCount;
    int underflowcount, overflowcount;
    vector<double> counts;

  };  
}

#endif
