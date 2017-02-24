{

  //change some input (fixed bin width) histograms to variable binning
  //input and output histograms are in the form: x y dy 
 
  //names of input and output files
  char * infile1 = "mtt.dat";
  char * infile2 = "pt.dat";
  char * infile3 = "y.dat";
  string * infiles[] = {infile1, infile2, infile3};

  int nfiles = sizeof(infiles)/sizeof(*infiles);

  char * outfile1 = "mtt_r.dat";
  char * outfile2 = "pt_r.dat";
  char * outfile3 = "y_r.dat";
  
  string * outfiles[] = {outfile1, outfile2, outfile3};

  //new bins for files 1, 2 and 3
  Double_t  newBins1[]={340,380,470,620,820,1100,1600};
  Double_t  newBins2[]={0,65,125,200,290,400};
  Double_t  newBins3[]={-2.5,-1.6,-1.0,-0.5,0.0,0.5,1.0,1.6,2.5};

  Double_t *newBins[] = {newBins1,newBins2,newBins3};

  //this is ugly, can we get no. of new bins a better way?
  int sizes[] = {sizeof(newBins1)/sizeof(*newBins1),
		 sizeof(newBins2)/sizeof(*newBins2),
		 sizeof(newBins3)/sizeof(*newBins3)};
  
  //default options:  pb/bin or fb/bin:      fb
  //                  divide by bin width?   Y     
  //                  normalise to unity?    Y
  //                  add overflow to last bin ??
  
  //define binning options
  bool pb = false;
  bool bin_width = true;
  bool normalise = true;
  bool overflow = true;

  //shouldn't need to edit anything below this line!
  std::vector<double> xs, ys, dys;
  for(int i=0; i<nfiles; i++){
  
    char * infile = infiles[i];
    std::ifstream fin(infile, ifstream::in);
    while(!fin.eof()){
      double xlo,xi,y,z;
      fin >> xlo >> xi >> y >> z;
      xs.push_back(xlo);
      ys.push_back(y);
      dys.push_back(z);
    }
    
    //get bin sizes, max and min x range: what about overflow?? 
    int nbins = xs.size()-1;
    double dx = fabs(xs.at(0)-xs.at(1));
    double xmin = xs.at(0);
    double xmax = xs.back()+dx;

    //store histograms in root objects
    TFile f("file.root","RECREATE"); 
    TH1F* h1 = new TH1F("h1","",nbins,xmin,xmax);
    for (int j=1;j<=nbins;j++) 
      {
	h1->SetBinContent(j,ys.at(j-1));
	h1->SetBinError(j,dys.at(j-1));
      }
    h1->Write();
    double xsec = h1->Integral();
    
    //do the rebinning  
    TH1F *h1_rebin = (TH1F*)h1->Rebin(sizes[i]-1,"",newBins[i]); 
    if(bin_width) h1_rebin->Scale(1,"Width");  
    if(normalise) h1_rebin->Scale(1/xsec);
    h1_rebin->Write();     
    
    //output to file
    char * outfile = outfiles[i];
    std::ofstream fout;
    
    fout.open(outfile);
    for (int k=1; k < h1_rebin->GetSize()-1; k++) { 
      if (pb) fout << h1_rebin->GetBinLowEdge(k) << "\t" << h1_rebin->GetBinLowEdge(k+1) << "\t" << h1_rebin->GetBinContent(k) << "\t" << h1_rebin->GetBinError(k) << endl;
      else    fout << h1_rebin->GetBinLowEdge(k) << "\t" << h1_rebin->GetBinLowEdge(k+1) << "\t" << 1000*h1_rebin->GetBinContent(k) << "\t" << 1000*h1_rebin->GetBinError(k) << endl;  
    }
    fout.close();

    //tidy up
    xs.clear();
    ys.clear();
    dys.clear();
    delete h1;
    delete h1_rebin;
    
  }
}

