#! /usr/bin/env python
import sys
import os
import array
from optparse import OptionParser
import ROOT

def main(): 

    parser = OptionParser()
    parser.add_option('-i','--input', action='store',type='string',dest='inputFile',default='../data/processed-pythia82-lhc13-all-pt1-50k-r1_h022_e0175_t220_nonu_truth.root', help='input file') 
    parser.add_option('-t','--tree', action='store',type='string',dest='tree'   ,default='t_allpar_new', help='tree name')
    parser.add_option('-o','--output', action='store',type='string',dest='outputDir'   ,default='train_simple/', help='output directory')
    (options,args) = parser.parse_args()
    
    if os.path.isdir(options.outputDir):
        print('output directory exists and will be over-written')
        os.rmdir(options.outputDir)
        os.mkdir(options.outputDir)
    else:
        os.mkdir(options.outputDir)
    
        fin    = ROOT.TFile(options.inputFile)
        inTree = fin.Get(options.tree)
        
        fout   = ROOT.TFile(options.outputDir+"train.root","RECREATE")
        ROOT.TMVA.Tools.Instance()
        factory = ROOT.TMVA.Factory("TMVAClassification",fout,
                                    ":".join([
                    "!V",
                    "!Silent",
                    "Color",
                    "DrawProgressBar",
                    "Transformations=I;D;P;G,D",
                    "AnalysisType=Classification"]
                                             ))
        
        factory.AddVariable("j_mass","F")
        factory.AddVariable("j_pt","F")
        factory.AddVariable("j_tau32_b1","F")
        factory.AddVariable("j_tau32_b2","F")

        factory.AddSignalTree(inTree)
        factory.AddBackgroundTree(inTree)

        sigCut= ROOT.TCut("(j_mass > 165 && j_mass < 250) && (j_tau32_b1 < 0.6 || j_tau32_b2 < 0.45)")
        bgCut = ROOT.TCut("(j_mass <= 165 || j_mass >= 250) && (j_tau32_b1 >= 0.6 || j_tau32_b2 >= 0.45)")
        
        factory.PrepareTrainingAndTestTree(sigCut,
                                           bgCut,
                                           ":".join([
                    "nTrain_Signal=0",
                    "nTrain_Background=0",
                    "SplitMode=Random",
                    "NormMode=NumEvents",
                    "!V"
                    ]))
        
        method = factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT",
                                    ":".join([
                    "!H",
                    "!V",
                    "NTrees=800",
                    "MinNodeSize=0.1",
                    "MaxDepth=3",
                    "BoostType=Grad",
                    "SeparationType=GiniIndex",
                    "nCuts=20",
                    "PruneMethod=NoPruning",
                    ]))
        
        factory.TrainAllMethods()
        factory.TestAllMethods()
        factory.EvaluateAllMethods()
    
if __name__ == '__main__':
    main();
