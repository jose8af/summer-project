import ROOT
import numpy as np

energy = '2500'
rootfile = f'../tuples/240817/{energy}_3ns_tuple.root'
file = ROOT.TFile.Open(rootfile)
bsm_tuple = file['B']
df = ROOT.RDataFrame('Tuple', bsm_tuple)
# %%

df.GetColumnNames()
# %%
c = ROOT.TCanvas()
#h = df.Histo1D("B_DTF_BestPVOnly_CHI2")
h = df.Histo1D(('chi2', 'chi2', 100, 0, 100), 'B_DTF_BestPVOnly_CHI2')
h.Draw()
c.Draw()
# %%

