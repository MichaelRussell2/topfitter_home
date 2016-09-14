# TOPFITTER Version 1

## 1. Prerequisties:

   * Python version > 2.7
   * gfortran (for MadEvent/MadAnalysis)
   * ROOT for rebinning (to be phased out)
   * professor2 (for fitting) and associated dependencies
   
## 2. Directory structure:

   * colliders: Input cards for MadEvent for the collider settings we are using

   * datasets: All the available fittable datasets. Each measurement is contained in
     	       a directory with the arXiv number of its publication as title. The
	       directory contains a folder called bins, containing the bin contents
	       of the measurements (optionally also a folder called corrs containing
	       bin correlations if they have also been published). There is also a
	       file called TAG, containing a brief description of the measurement
	       (typically this is just the paper title) and a file called settings,
	       containing the experiment name, collider type and process description,
	       e.g. ATLAS,LHC8,ttZ.

To add a new measurement, use the script ./make_datadir in the datasets
directory. For consisitency make the measurement directory name the arXiv
number, e.g. ./make_datadir 1101.1001 --coll TEVT --expt D0 --proc ttbar

   * fitting: The various professor scripts used for fitting/limit-setting

   * kfactors: (N)NLO QCD K-factors for the processes of interest, to reweight the
                   leading order Monte Carlo predictions

   * models: All (1) of the models that we have to fit so far. Hopefully there will
     	     be more one day!

   * processes: Tarballs of the MadEvent directories for all the processes we
     		consider here

   * scripts: Various scripts needed throughout the analysis chain. More details on
     	      each in the next section

## 3. Getting started

To initialise a new dataset directory, run the script ./topfitter_init, e.g.
   `./topfitter_init new_measurement_name --proc ttZ --coll LHC13 --dat 1510.05302`

Use the `list-foo` options to see available datasets/processes. This command will
make a new directory, with the following scripts

     * generate_space.py: Generate the parameter space to sample the points from.
       			    Additional options can be given here, e.g. number of
			    sample points, number of dimensions, boundaries of the
			    space, logarithmic or linear sampling.

     * run_scan.py: Start generating the samples, only choice here is the number of
       		      scan points, and whether or not to also plot events with
		      MadAnalysis. You'll need to look into the script yourself to
		      ensure that the right operators are being given to MadEvent.
		      Alternatively if you have access to a batch farm, you can use the
		      script make_batchgrid.py to make a grid of points that can be set
		      to run in parallel with your own PBS submission script.

For MadAnalysis settings, edit the file `ma_card.dat` in the MadAnalysis directory.
Be careful about the binning though 
(as described later)

For storage reasons, the events are deleted after plotting. To change this, edit the
`run_scan.py` file

Once the events are finished plotting, a directory called plots contains the
histograms from every run. These are in topdrawer format. To convert these to plain
.dat format, use the `make_plots.sh` file, which in turn calls the `extract_dats`
script, converting topdrawer to plain dat format (see comments in that
file for how to use it)

Then the leading order predictions are NLO reweighted with the `nlo_reweight.py`
script. You shouldn't need to change anything here. The binning of the plots must
have the same binning as the binning of the kfactors. By default, this is very fine,
so that the same samples can be used to fit measurements with the same collider
settings but different binning (e.g. the same samples can be used for both ATLAS and
CMS 7 TeV ttbar data). This is only sensible for unfolded, parton-level (no cuts)
'measurements', of course.

Next, rebin the histograms. Edit the `rebin.cc` script to the binning/histogram names
that you need, then run `rebin_all.sh` to loop over all the sample points. 

Now the data can be converted for use with professor. See the scripts in the fitting
directory. In particular, use `fittabledata2prof` to convert data to YODA, then
`prof2-ipol` (part of professor v2) to make the interpolation polynomial, then
`ipol2chi2-1d` or variations thereof to get the constraints. 

Try the full analysis chain with a small number (e.g < 50) sample points to get the
hang of it. Tell me about any bugs!
