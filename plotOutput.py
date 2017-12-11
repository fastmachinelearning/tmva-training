#! /usr/bin/env python
import sys
import os
import array
from optparse import OptionParser
import ROOT

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option('-i','--input', action='store',type='string',
                      dest='inputFile',default='train_simple/train.root', help='input file') 
    parser.add_option('-t','--tree1', 
                      action='store',type='string',
                      dest='tree1',default='TrainTree', help='tree name')
    parser.add_option('-g','--tree2', 
                      action='store',type='string',
                      dest='tree2',default='TestTree', help='tree name')
    parser.add_option('-o','--output', 
                      action='store',type='string',dest='outputDir',
                      default='output/', help='output directory')
    (options,args) = parser.parse_args()
    
    if os.path.isdir(options.outputDir):
        print('output directory exists and will be over-written')
        os.rmdir(options.outputDir)
        os.mkdir(options.outputDir)
    else:
        os.mkdir(options.outputDir)
    
        fin    = ROOT.TFile(options.inputFile)

        hTrainSig = ROOT.TH1D('hTrainSig','S (Train)',20,-1.0,1.0)
        hTrainBkg = ROOT.TH1D('hTrainBkg','B (Train)',20,-1.0,1.0)
        hTestSig  = ROOT.TH1D('hTestSig','S (Test)',20,-1.0,1.0)
        hTestBkg  = ROOT.TH1D('hTestBkg','B (Test)',20,-1.0,1.0)
        
        vhists = [ hTrainBkg, hTrainSig, hTestBkg, hTestSig ]
        
        for h in vhists :
            h.Sumw2();

        TrainTree = fin.Get(options.tree1)
        TestTree  = fin.Get(options.tree2)

        for ientry in TrainTree :
            if ((ientry.j_mass > 165 and ientry.j_mass < 250) and (ientry.j_tau32_b1 < 0.6 or ientry.j_tau32_b2 < 0.45)) :
                hTrainSig.Fill(ientry.BDT)
            else:
                hTrainBkg.Fill(ientry.BDT)
                
        for ientry in TestTree :
            if ((ientry.j_mass > 165 and ientry.j_mass < 250) and (ientry.j_tau32_b1 < 0.6 or ientry.j_tau32_b2 < 0.45)) :
               hTestSig.Fill(ientry.BDT)
            else:
                hTestBkg.Fill(ientry.BDT)
                
        
        
        for h in vhists :
            if h.Integral() != 0: h.Scale(1/h.Integral());
                
        # Create the color styles
        hTrainSig.SetLineColor(ROOT.kRed)
        hTrainSig.SetMarkerColor(ROOT.kRed)
        hTrainSig.SetFillColor(ROOT.kRed)
        hTestSig.SetLineColor(ROOT.kRed)
        hTestSig.SetMarkerColor(ROOT.kRed)
        hTestSig.SetFillColor(ROOT.kRed)
 
        hTrainBkg.SetLineColor(ROOT.kBlue)
        hTrainBkg.SetMarkerColor(ROOT.kBlue)
        hTrainBkg.SetFillColor(ROOT.kBlue)
        hTestBkg.SetLineColor(ROOT.kBlue)
        hTestBkg.SetMarkerColor(ROOT.kBlue)
        hTestBkg.SetFillColor(ROOT.kBlue)
 
        # Histogram fill styles
        hTrainSig.SetFillStyle(3004)
        hTrainBkg.SetFillStyle(3005)
        hTestSig.SetFillStyle(0)
        hTestBkg.SetFillStyle(0)
 
        # Histogram marker styles
        hTestSig.SetMarkerStyle(20)
        hTestBkg.SetMarkerStyle(20)
 
        # Set titles
        hTrainSig.GetXaxis().SetTitleOffset(1.1)
        hTrainSig.GetXaxis().SetTitle("BDT output")
        hTrainSig.GetYaxis().SetTitleOffset(1.2)
        hTrainSig.GetYaxis().SetTitle("a.u.")
        
        # Draw the objects
        c1 = ROOT.TCanvas("c1","",800,600)
        ROOT.gStyle.SetOptStat(0)
        ROOT.gStyle.SetOptTitle(0)
        ROOT.gStyle.SetLegendBorderSize(0)
        c1.cd(1).SetLogy()
        hTrainSig.Draw("HIST")
        hTrainBkg.Draw("HISTSAME")
        hTestSig.Draw("EPSAME")
        hTestBkg.Draw("EPSAME")
 
        # Reset the y-max of the plot
        ymax = max([ h.GetMaximum() for h in vhists ])
        ymax *=1.5
    
        hTrainSig.SetMaximum(ymax)
        hTrainSig.SetMinimum(2e-8*ymax)
        # Create Legend
        c1.cd(1).BuildLegend( 0.57,  0.72,  0.72,  0.88).SetFillColor(0)
 
        # Add custom title
        l1=ROOT.TLatex()
        l1.SetNDC();
        l1.DrawLatex(0.26,0.93,"Simple training")
 
        # Finally, draw the figure
        c1.Print(options.outputDir+'BDT_output.png')    
