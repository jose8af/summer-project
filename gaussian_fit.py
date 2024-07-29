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
rootfile = f'tuples/{filename}.root'
file = ROOT.TFile.Open(rootfile)
filetuple = file['Higgs']
treename = 'Tuple'
df = ROOT.RDataFrame(treename, filetuple)

# Define the mass observable
x = ROOT.RooRealVar('x', 'mass observable', 0, 5000)
roo_data_set_hmass = df.Book(ROOT.std.move(ROOT.RooDataSetHelper('dataset', 'h mass', ROOT.RooArgSet(x))), (['H_MASS']))
data = roo_data_set_hmass.GetValue()

# %%

mean = ROOT.RooRealVar('mean', 'mean of all gaussians', 2500, 2495, 2505)

# Adjusted parameter ranges and initial values
sigma1 = ROOT.RooRealVar('sigma1', 'sigma of first gaussian', 80, 1, 1000)
gauss1 = ROOT.RooGaussian('gauss1', 'gauss1(x,mean,sigma1)', x, mean, sigma1)

sigma2 = ROOT.RooRealVar('sigma2', 'sigma of second gaussian', 120, 1, 1000)
gauss2 = ROOT.RooGaussian('gauss2', 'gauss2(x,mean,sigma2)', x, mean, sigma2)

# Optional third Gaussian to capture more details
sigma3 = ROOT.RooRealVar('sigma3', 'sigma of third gaussian', 200, 1, 1000)
gauss3 = ROOT.RooGaussian('gauss3', 'gauss3(x,mean,sigma3)', x, mean, sigma3)


frac_gaussian1= ROOT.RooRealVar("frac_gaussian1", "fraction of first gaussian", 0.6, 0.0, 1.0)
frac_gaussian2 = ROOT.RooRealVar("frac_gaussian2", "fraction of second gaussian", 0.6, 0.0, 1.0)

model = ROOT.RooAddPdf("model", "triple gaussian",
                       ROOT.RooArgList(gauss1, gauss2, gauss3),
                       ROOT.RooArgList(frac_gaussian1, frac_gaussian2))

# Fit the model to the data
model.fitTo(data, ROOT.RooFit.Range(0, 5000), ROOT.RooFit.Minimizer("Minuit2", "migrad"))

# Plot the data and the fit result
c = ROOT.TCanvas('triple', 'triple gauss', 1200, 1000)
xframe = x.frame(ROOT.RooFit.Range(0, 5000))
xframe.SetTitle(f'Triple Gaussian {filename} Fit')
data.plotOn(xframe, ROOT.RooFit.Binning(200))
model.plotOn(xframe)
model.paramOn(xframe, ROOT.RooFit.Layout(0.6, 0.9, 0.9))
xframe.Draw()
c.Draw()
c.SaveAs(f'plots/triple_gauss/{filename}.png')



# %%

pull_frame = x.frame()

pull_frame.SetTitle("Pull Distribution triple gaussian")

# Plot the pull distribution
pull_hist = xframe.pullHist()
pull_frame.addPlotable(pull_hist, "P")

# Draw the pull distribution
c2 = ROOT.TCanvas("c2", "Pull Distribution", 800, 600)

pull_frame.Draw()

c2.Draw()
c2.SaveAs(f'plots/triple_gauss/pull_{filename}.png')

# %%

