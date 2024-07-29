# %%
#filename = '0500_3ns_tuple'    
#filename = '1500_3ns_tuple' 
filename = '2500_3_dtf'
#filename = '2500_3ns_tuple' 
#filename = '3500_3_dtf' 
#filename =  '3500_3ns_tuple' 
#filename = '4500_3ns_tuple'


# %%
import ROOT
rootfile = f'/home/josedavid8af/8A/code/summer-project/summer-project/tuples/{filename}.root'
file = ROOT.TFile.Open(rootfile)
filetuple = file['Higgs']
treename = 'Tuple'
df = ROOT.RDataFrame(treename, filetuple)

x = ROOT.RooRealVar('x','mass observable', 0, 4500)
roo_data_set_hmass = df.Book(ROOT.std.move(ROOT.RooDataSetHelper('dataset', 'h mass' , ROOT.RooArgSet(x))), (['H_MASS']))
data = roo_data_set_hmass.GetValue()

# %%
mu = ROOT.RooRealVar("mu", "mu", 2500, 2495, 2505)

alpha = ROOT.RooRealVar("alpha", "alpha", 1.0, 0, 50.0)
n = ROOT.RooRealVar("n", "n", 5, 0, 100)
sigma = ROOT.RooRealVar("sigma", "sigma", 100, 0, 500)

alpha2 = ROOT.RooRealVar("alpha2", "alpha", 1.0, 0, 50.0)
n2 = ROOT.RooRealVar("n2", "n", 5, 0, 500)
sigma2 = ROOT.RooRealVar("sigma2", "sigma", 100, 0, 1000)

alpha3 = ROOT.RooRealVar("alpha3", "alpha", 1.0, 0, 50.0)
n3 = ROOT.RooRealVar("n3", "n", 5, 0, 500)
sigma3 = ROOT.RooRealVar("sigma3", "sigma", 100, 0, 1000)


# Define the Crystal Ball PDF
crystalball1 = ROOT.RooCrystalBall("crystalball1", "crystalball", x, mu, sigma, alpha, n)
crystalball2 = ROOT.RooCrystalBall("crystalball2", "crystalball", x, mu, sigma2, alpha2, n2)
crystalball3 = ROOT.RooCrystalBall("crystalball3", "crystalball", x, mu, sigma3, alpha3, n3)

frac_crystal = ROOT.RooRealVar("frac_crystal", "fraction of first crystal", 0.6, 0.0, 1.0)
frac_crystal2 = ROOT.RooRealVar("frac_crystal2", "fraction of first crystal", 0.6, 0.0, 1.0)


model = ROOT.RooAddPdf("model", "double crystal",
                       ROOT.RooArgList(crystalball1, crystalball2, crystalball3),
                       ROOT.RooArgList(frac_crystal, frac_crystal2))

# Fit the model to the data
model.fitTo(data, ROOT.RooFit.Range(0, 4500), ROOT.RooFit.Minimizer("Minuit2", "migrad"))

# Plot the data and the fit result
c = ROOT.TCanvas('crystal', 'crystal', 1200, 1000)
xframe = x.frame(ROOT.RooFit.Range(0, 5000))
xframe.SetTitle(f'Triple {filename} Crystal Ball Fit')
data.plotOn(xframe, ROOT.RooFit.Binning(200))
model.plotOn(xframe)
model.paramOn(xframe, ROOT.RooFit.Layout(0.6, 0.9, 0.9))
xframe.Draw()
c.SaveAs(f'plots/triple_crystal/{filename}.png')

# %%
pull_frame = x.frame()

pull_frame.SetTitle("Pull Distribution triple crys")

# Plot the pull distribution
pull_hist = xframe.pullHist()
pull_frame.addPlotable(pull_hist, "P")

# Draw the pull distribution
c2 = ROOT.TCanvas("c2", "Pull Distribution", 800, 600)

pull_frame.Draw()
c2.SaveAs(f'plots/triple_crystal/pull_{filename}.png')

# %%


