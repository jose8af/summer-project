import ROOT
import numpy as np

energy = '2.5'
rootfile = f'../tuples/BSM_tuple_H2MuMu_{energy}GeV3nsNoGenCut.root'
file = ROOT.TFile.Open(rootfile)
bsm_tuple = file['B']
df = ROOT.RDataFrame('Tuple', bsm_tuple)

variables = ['B_BKGCAT','B_END_VZ','B_END_VX','B_END_VY','B_END_VRHO','B_BPVCORRM','B_BPVDIRA','B_BPVETA','B_BPVIPCHI2','B_BPVFDCHI2','B_BPVLTIME','B_BPVFD','B_BPVFDIRX','B_BPVFDIRY','B_BPVFDIRZ','B_BPVFDVECX','B_BPVFDVECY','B_BPVFDVECZ','B_BPVIP','B_BPVVDRHO','B_BPVVDX','B_BPVVDY','B_BPVVDZ', 'B_M','B_P','B_PT','B_PX','B_PY','B_PZ','B_ENERGY','B_ETA','K_plus_MASS','K_plus_CHI2','K_plus_M','K_plus_P','K_plus_PT','K_plus_PX','K_plus_PY','K_plus_PZ','K_plus_ENERGY','K_plus_ETA','K_plus_MINIP','K_plus_MINIPCHI2','K_plus_QOVERP','K_plus_ECALPIDE','K_plus_ECALPIDMU','K_plus_ELECTRONENERGY','K_plus_ELECTRONID','K_plus_ELECTRONSHOWEREOP','K_plus_HCALEOP','K_plus_HCALPIDE','K_plus_HCALPIDMU','K_plus_TX','K_plus_TY','K_plus_BPVX','K_plus_BPVY','K_plus_BPVZ','K_plus_CHARGE','K_plus_GHOSTPROB','K_plus_PID_P','K_plus_PID_PI','K_plus_PID_K','K_plus_PID_MU','K_plus_PID_E','H_M']

tuple_array = df.AsNumpy(variables)
variable = 'H_M' 

bck_array = tuple_array[variable][tuple_array['B_BKGCAT'] == 100]
set_array = tuple_array[variable][tuple_array['B_BKGCAT'] == 70]
signal_array = tuple_array[variable][tuple_array['B_BKGCAT'] == 30]

axis_name = r'Higgs #rightarrow (H^{*})#mu^{+}#mu^{-}'
hist1 = ROOT.TH1F("hist1", f"{axis_name} for bkgcat=100", 100, bck_array.min(), bck_array.max())
hist2 = ROOT.TH1F("hist2", f"{variable} for bkgcat=30", 100, signal_array.min(), signal_array.max())
hist3 = ROOT.TH1F("hist3", f"{variable} for bkgcat=set", 100, set_array.min(), set_array.max())

for value in bck_array:
    hist1.Fill(value)

for value in signal_array:
    hist2.Fill(value)

for value in set_array:
    hist3.Fill(value)

hist1.SetLineColor(ROOT.kRed)
hist2.SetLineColor(ROOT.kBlue)
hist3.SetLineColor(ROOT.kGreen)



c1 = ROOT.TCanvas("c1", "Histogram Canvas", 800, 600)
hist1.Draw()
hist2.Draw("SAME")
hist3.Draw('SAME')

legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(hist1, "bkgcat=100", "l")
legend.AddEntry(hist2, "bkgcat=30", "l")
legend.AddEntry(hist3, "bkgcat=70", "l")
legend.Draw()

c1.SaveAs(f'{variable}.png')

# %%

