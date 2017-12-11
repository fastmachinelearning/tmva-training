#! /usr/bin/env python
import sys
import os
import array
from optparse import OptionParser
import ROOT

def makeCanvas(hs,legs,name,outdir):
    colors = [1,2,4,6,7];
    maxval = -999;

    for h in hs:
        if h.Integral() != 0: h.Scale(1/h.Integral());
        h.SetLineWidth(2);
        if h.GetMaximum() > maxval: maxval =  h.GetMaximum()

    leg = ROOT.TLegend(0.5,0.7,0.7,0.9)
    leg.SetBorderSize(0);
    leg.SetFillStyle(0);
    leg.SetTextSize(0.035);
    i = 0;
    for h in hs:
        leg.AddEntry(h,legs[i],"l")
        i+=1;

    c = ROOT.TCanvas("c","c",1000,800);
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    hs[0].SetMaximum(maxval*1.5);
    hs[0].Draw("hist");
    i = 0;
    for h in hs:
        h.SetLineColor(colors[i])
        h.Draw("histsames");
        i+=1;
    leg.Draw();

    l1=ROOT.TLatex()
    l1.SetNDC();
    l1.DrawLatex(0.26,0.93,name[0][:-2])

    c.SetLogy(1);
    c.SaveAs(outdir+name[0][:-2]+".pdf");
    c.SaveAs(outdir+name[0][:-2]+".png");

def main(): 

    parser = OptionParser()
    parser.add_option('-i','--input', action='store',type='string',dest='inputFile',default='../data/processed-pythia82-lhc13-all-pt1-50k-r1_h022_e0175_t220_nonu_truth.root', help='input file') 
    parser.add_option('-t','--tree', action='store',type='string',dest='tree'   ,default='t_allpar_new', help='tree name')
    parser.add_option('-o','--output', action='store',type='string',dest='outputDir'   ,default='inputvars/', help='output directory')
    (options,args) = parser.parse_args()
    
    if os.path.isdir(options.outputDir):
        print('output directory exists and will be over-written')
        os.rmdir(options.outputDir)
        os.mkdir(options.outputDir)
    else:
        os.mkdir(options.outputDir)
    
        fin    = ROOT.TFile(options.inputFile)
        inTree = fin.Get(options.tree)

        hj_mass_S     = ROOT.TH1D('hj_mass_S','jmass',50,0.0,500.0)
        hj_pt_S       = ROOT.TH1D('hj_pt_S', 'jpt', 50,0.0,1000.0)
        hj_tau32_b1_S = ROOT.TH1D('hj_tau32_b1_S', 'jtau32_b1', 50,0.0,1.0)
        hj_tau32_b2_S = ROOT.TH1D('hj_tau32_b2_S', 'jtau32_b2', 50,0.0,1.0)

        hj_mass_B     = ROOT.TH1D('hj_mass_B','jmass',50,0.0,500.0)
        hj_pt_B       = ROOT.TH1D('hj_pt_B', 'jpt', 50,0.0,1000.0)
        hj_tau32_b1_B = ROOT.TH1D('hj_tau32_b1_B', 'jtau32_b1', 50,0.0,1.0)
        hj_tau32_b2_B = ROOT.TH1D('hj_tau32_b2_B', 'jtau32_b2', 50,0.0,1.0)

        
        for ientry in inTree :
            if inTree.j_t == 1 :
                hj_mass_S.Fill(inTree.j_mass)
                hj_pt_S.Fill(inTree.j_pt)
                hj_tau32_b1_S.Fill(inTree.j_tau32_b1)
                hj_tau32_b2_S.Fill(inTree.j_tau32_b2)
            else :
                hj_mass_B.Fill(inTree.j_mass)
                hj_pt_B.Fill(inTree.j_pt)
                hj_tau32_b1_B.Fill(inTree.j_tau32_b1)
                hj_tau32_b2_B.Fill(inTree.j_tau32_b2)

        vjmass      = [ hj_mass_S , hj_mass_B ] 
        vjpt        = [ hj_pt_S , hj_pt_B ] 
        vjtau32b1 = [ hj_tau32_b1_S , hj_tau32_b1_B ] 
        vjtau32b2 = [ hj_tau32_b2_S , hj_tau32_b2_B ] 

        pName_jmass    = [ 'jmass_S', 'jmass_B' ]
        pName_jpt      = [ 'jpt_S', 'jpt_B' ]
        pName_jtau32b1 = [ 'jtau32b1_S', 'jtau32b1_B' ]
        pName_jtau32b2 = [ 'jtau32b2_S', 'jtau32b2_B' ]
        
        leg1 = ['tt', 'other']

        makeCanvas( vjmass,leg1,pName_jmass,options.outputDir )
        makeCanvas( vjpt,leg1,pName_jpt,options.outputDir )
        makeCanvas( vjtau32b1,leg1,pName_jtau32b1,options.outputDir )
        makeCanvas( vjtau32b2,leg1,pName_jtau32b2,options.outputDir )
     
if __name__ == '__main__':
    main();
