# Measurements to add (taken from TopFitter twiki data page)

## 1. Parton level / full phase-space

   * 1508.03862: ttbar charge asymmetry, inclusive @ 8 TeV. Value in abstract.

   * 1507.03119: ttbar charge asymmetry, inclusive and differential in |y(t,tbar)|  
     		 and m(t,tbar). Two different binnings for latter, only use one.
		 Figure 5, page 10, **HepData available**

   * 1601.01107: distributions in dilepton ttbar events sensitive to spin correlations
     		 figure 3, page 12: delta phi between leptons; and other angles
		 described in text. **HepData available**
		 
   * 1511.02138: spin asymmetry in t-channel single top production, with decays
     		 to muons, extracted from
     		 normalised differential cross-section as a function of cos_thetastar
		 where thetastar is the angle between the muon from the top decay and
		 the untagged jet, with all four-momenta defined in the top rest frame
		 Plots on page 15, figure 6, and **HepData available**

   * 1607.00837: ttbar differential cross-sections in l+jets channel and 7 and 8 TeV
     		 plotted as a function of ETmiss, pT of the leptonic W, HT and 
		 ST = HT + ETmiss + pTlepton
		 tag as ttbar_s, generated decayed lepton+jets samples
		 Data on pages 19-22, Table A

## 2. Particle level / fiducial phase-space

   * 1508.06868: Fiducial total cross-sections for ttbar + up to 2 b-tagged jets
     		 Data on pg 32, Tab 15: use cut-based numbers only  
     		 **No Rivet analysis available**  
		 **Need to generate merged samples**

   * 1407.0891: ttbar differential cross-sections with additional jets
		Distributions in mu+jets and e+jets channel of: number of jets
		Plots on pages 27-31, figs 6-10:
		Cross-section as a function of leading, 2nd, 3rd, 4th and 5th jet pT
		for a jet pT threshold of 25 GeV and as a function of jet multiplicity
		for jet pT thresholds of 25, 40, 60 and 80 GeV
		**HepData and Rivet analysis available**
		**Need to generate merged signal samples with up to 5 additonal jets**

   * 1203.5015: ttbar differential cross-sections with central jet veto
     		NO Cross-sections plotted here, instead the *gap fractions*
		f(Q_0) = the ratio of the ttbar cross-section for events produced
		**WITHOUT** an additional jet of pT > Q_0 (in a certain rapidity region
		, to the fiducial ttbar cross-section
		and f(Q_sum); the ratio of the ttbar cross-section for events produced
		with a scalar sum of the pTs of the additional jets < Q_sum
		Rapidity intervals: <0.8, 0.8 < |y| < 1.5, 1.5 < |y| < 2.1 and > 2.1
		are considered
		Plots in figures 4-6, pages 8-10, data in tables 2 and 3, page 11
		**Rivet analysis available**
		**Need to generate merged samples**

   * 1404.3171: ttbar differential cross-section versus number of additional jets
     		in dilepton channel for jet pT > 35 GeV and > 60 GeV
		and lepton+jets channel: additional jets have pT theshold > 35 GeV
		Up to 8 additional jets are considered
		Data in Tab1-3, pg 10 and Figures 2 and 3, pg 11-12
		**Rivet analysis available**
		**Need to generate merged samples, up to 8 jets!?**

    
---

## Measurements that have not been listed here have been excluded, for one of the
   following reasons:

   * Data is not tabulated in paper or HepData; would need to read data from plots  
   * Data is not background subtracted, would need to generate backgrounds as well
   * Measurement is made using model-specific assumptions we want to avoid
   * Measurement is made using a not-reproducible BDT-based analysis
   * Particular observable is not sensitive to interference with dimension-six operators
   * Analysis is a search and not a measurement, so no signal data to unfold
   