#include <histo.hh>

//@TODO: rebin, histeps option, setw
//FastPartons::Histo::Histo() {}
//FastPartons::Histo::~Histo() {}


//the 1D histogram constructor
FastPartons::Histo::Histo(const double xmin, const double xmax, const double deltax){
  min = xmin;
  max = xmax;
  binWidth = deltax;
  binCount = (int)((max-min)/binWidth);
  weights = vector<double>(binCount,0);
  counts = vector<int>(binCount,0);
  weightsOver = 0.;
  weightsUnder = 0.;
  countsOver = 0;
  countsUnder = 0;
  useErrors = false;
}

//fill histo with number of events only
void FastPartons::Histo::fill(double entry) {
  if (entry < min) {
    weightsUnder += 1.;
    countsUnder++;
    return;
  } 
  else if (entry > max) {
    weightsOver += 1.;
    countsOver++;
    return;
  } 
  else {
    int bin = (int)((entry - min) / binWidth);
    weights[bin]+=1.;
    counts[bin]++;
  }
}

//fill histo with event weights
void FastPartons::Histo::fill(double entry, double weight) {
  if ( entry < min ) {
    weightsUnder += weight;
    countsUnder++;
    return;
  }
  else if ( entry > max ){
    weightsOver += weight;
    countsOver++;
    return;
  }
  int bin = (int)((entry - min) / binWidth);
  weights[bin]+=weight;
  counts[bin]++;
  return;
}


//write out raw histogram
void FastPartons::Histo::write(const char *outfile){
 std::ofstream fout;
 fout.open(outfile);
 //add MC stats error as column 4
 if (useErrors){
   for (int i=0; i<binCount; i++){
     double binErr = counts[i] != 0 ? weights[i]/sqrt(counts[i]) : 0.;
     fout << lowerBound(i) << "  " << upperBound(i) << "  " << weights[i] << "  " << binErr << endl;
   }
 }
 //default is 3 columns
 else{
   for (int i=0; i<binCount; i++){
     fout << lowerBound(i) << "  " << upperBound(i) << "  " << weights[i] << endl;
   }
 }
 fout.close();
 weights.clear();
}

//write out normalised histogram
void FastPartons::Histo::write(const char *outfile, double norm){
 std::ofstream fout;
 fout.open(outfile);
  for (int i=0; i<binCount; i++){
    fout << lowerBound(i) << "  " << upperBound(i) << "  " << weights[i]/norm << endl;
  }
  fout.close();
  weights.clear();
}

//underflow
double FastPartons::Histo::underflow(){
  return weightsUnder;
}

//overflow
double FastPartons::Histo::overflow(){
  return weightsOver;
}

//add underflow to first bin
void FastPartons::Histo::addUnderflow(){
  weights[0] += weightsUnder;
  counts[0] += countsUnder;
  return;
}

//add overflow to last bin
void FastPartons::Histo::addOverflow(){
  weights[binCount-1] += weightsOver;
  counts[binCount-1] += countsOver;
  return;
}

//lower edge of bin
double FastPartons::Histo::lowerBound(int bin){
  return (min+bin*binWidth);
}

//upper edge of bin
double FastPartons::Histo::upperBound(int bin){
  return (min+(bin+1)*binWidth);
}

//integral of a 1d histogram
double FastPartons::Histo::integral(){
  double area = 0;
  for (int i=0; i<binCount; i++){
    area += weights[i];
  }
  return area;
}

//flag to switch on bin errors
void FastPartons::Histo::sumw2(){
  useErrors=true;
  return;
}

//2D HISTOGRAM MEMBERS

//the 2D histogram constructor
//@TODO: inherit from 1D histo???
FastPartons::Histo2d::Histo2d(const double xmin, const double xmax, const double deltax, const double ymin, const double ymax, const double deltay){
  minx = xmin;
  maxx = xmax;
  miny = ymin;
  maxy = ymax;
  binWidthx = deltax;
  binWidthy = deltay;
  binCountx = (int)((maxx-minx)/binWidthx);
  binCounty = (int)((maxy-miny)/binWidthy);
  weights2d = vector< vector<double> > (binCountx, vector<double>(binCounty,0));
}

//fill 2d histo
void FastPartons::Histo2d::fill(double xentry, double yentry) {
  if ( xentry < minx || xentry > maxx || yentry < miny || yentry > maxy ) return;
  int binx = (int)((xentry - minx) / binWidthx);
  int biny = (int)((yentry - miny) / binWidthy);
  weights2d[binx][biny] += 1;
  return;
}

//fill 2d histo with event weights
void FastPartons::Histo2d::fill(double xentry, double yentry, double weight) {
  if ( xentry < minx || xentry > maxx || yentry < miny || yentry > maxy ) return;
  int binx = (int)((xentry - minx) / binWidthx);
  int biny = (int)((yentry - miny) / binWidthy);
  weights2d[binx][biny] += weight;  
  return;
}

//write out raw 2d histogram
void FastPartons::Histo2d::write(const char *outfile){
 std::ofstream fout;
 fout.open(outfile);
  for (int i=0; i<binCountx; i++){
    for (int j=0; j<binCounty; j++){
      fout << lowerBoundx(i) << "  " << upperBoundx(i) << "  " << lowerBoundy(j) << "  " << upperBoundy(j) << "  " << weights2d[i][j]  << endl;
    }
  }
  fout.close();
  weights2d.clear();
}

//write out normalized 2d histogram
void FastPartons::Histo2d::write(const char *outfile, double norm){
 std::ofstream fout;
 fout.open(outfile);
  for (int i=0; i<binCountx; i++){
    for (int j=0; j<binCounty; j++){
      fout << lowerBoundx(i) << "  " << upperBoundx(i) << "  " << lowerBoundy(j) << "  " << upperBoundy(j) << "  " << weights2d[i][j]/norm  << endl;
    }
  }
  fout.close();
  weights2d.clear();
}


//integral of a 2d histogram
double FastPartons::Histo2d::integral(){
  double volume = 0;
  for (int i=0; i<binCountx; i++){
    for (int j=0; j<binCounty; j++){
      volume += weights2d[i][j];
    }
  }
  return volume;
}

//lower x bin edge
double FastPartons::Histo2d::lowerBoundx(int bin){
  return (minx+bin*binWidthx);
}

//upper x bin edge
double FastPartons::Histo2d::lowerBoundy(int bin){
  return (miny+bin*binWidthy);
}

//lower y bin edge
double FastPartons::Histo2d::upperBoundx(int bin){
  return (minx+(bin+1)*binWidthx);
}

//upper y bin edge
double FastPartons::Histo2d::upperBoundy(int bin){
  return (miny+(bin+1)*binWidthy);
}
