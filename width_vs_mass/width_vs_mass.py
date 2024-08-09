# %%
import ROOT
#energy = ['500', '1500', '2500', '3500', '4500']
energy = '4500'
variable = 'H_DTF_BestPV_MASS' #H_DTF_BestPVOnly_MASS , H_M
ini_range = int(energy) - 100 
fin_range = int(energy) + 100

rootfile = f'../tuples/{energy}_3ns_tuple.root'
file = ROOT.TFile.Open(rootfile)
filetuple = file['B']
df = ROOT.RDataFrame('Tuple', filetuple)

x = ROOT.RooRealVar('x','mass observable', ini_range, fin_range)
roo_data_set_hmass = df.Book(ROOT.std.move(ROOT.RooDataSetHelper('dataset', variable , ROOT.RooArgSet(x))), ([variable]))
data = roo_data_set_hmass.GetValue()


mu = ROOT.RooRealVar("mu", "mu", int(energy), int(energy)-3 , int(energy)+3)

alpha = ROOT.RooRealVar("alpha", "alpha", 1.0, 0, 500)
n = ROOT.RooRealVar("n", "n", 5, 0, 500)
sigma = ROOT.RooRealVar("sigma", "sigma", 100, 0, 500)

alpha2 = ROOT.RooRealVar("alpha2", "alpha", 1.0, 0, 500)
n2 = ROOT.RooRealVar("n2", "n", 5, 0, 500)
sigma2 = ROOT.RooRealVar("sigma2", "sigma", 100, 0, 500)

crystalball1 = ROOT.RooCrystalBall("crystalball1", "crystalball", x, mu, sigma, alpha, n, True)
crystalball2 = ROOT.RooCrystalBall("crystalball2", "crystalball", x, mu, sigma2, alpha2, n2, True)

frac_crystal = ROOT.RooRealVar("frac_crystal", "fraction of first crystal", 0.6, 0.0, 1.0)

model = ROOT.RooAddPdf("model", "double crystal",
                       ROOT.RooArgList(crystalball1, crystalball2),
                       ROOT.RooArgList(frac_crystal))

model.fitTo(data, ROOT.RooFit.Range(ini_range, fin_range), ROOT.RooFit.Minimizer("Minuit2", "migrad"))

c = ROOT.TCanvas('crystal', 'crystal', 800, 600)
xframe = x.frame(ROOT.RooFit.Range(ini_range, fin_range))
xframe.SetTitle(f'{energy} {variable} Double Crystal Ball Fit')
data.plotOn(xframe, ROOT.RooFit.Binning(150))
model.plotOn(xframe)
model.paramOn(xframe, ROOT.RooFit.Layout(0.6, 0.9, 0.9))
xframe.Draw()
c.SaveAs(f'plots/{variable}/{energy}.png')

with open(f"fit_results/{variable}/{energy}.txt", "w") as f:
    f.write(f"frac1: {frac_crystal.getVal()} ± {frac_crystal.getError()}\n")
    f.write(f"mu: {mu.getVal()} ± {mu.getError()}\n")
    f.write(f"Sigma1: {sigma.getVal()} ± {sigma.getError()}\n")
    f.write(f"Sigma2: {sigma2.getVal()} ± {sigma2.getError()}\n")
    f.write(f"alpha1: {alpha.getVal()} ± {alpha.getError()}\n")
    f.write(f"alpha2: {alpha2.getVal()} ± {alpha2.getError()}\n")
    f.write(f"n: {n.getVal()} ± {n.getError()}\n")
    f.write(f"n2: {n2.getVal()} ± {n2.getError()}\n") 
   
pull_frame = x.frame()

pull_frame.SetTitle(f"Pull Dist. Double Cryst {energy}")

# Plot the pull distribution
pull_hist = xframe.pullHist()
pull_frame.addPlotable(pull_hist, "P")

# Draw the pull distribution
c2 = ROOT.TCanvas("c2", "Pull Distribution", 800, 600)

pull_frame.Draw()
c2.SaveAs(f'plots/{variable}/pull_{energy}.png')


# %%
import matplotlib.pyplot as plt
import os

def read_fit_results(filename):
    """Read fit results from a given filename and return a dictionary of values."""
    results = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.split(':')
            value = value.split('±')[0].strip()  # Take only the value, not the error
            results[key.strip()] = float(value)
    return results

def compute_combined_sigma(frac, sigma1, sigma2):
    """Compute the combined sigma using the provided formula."""
    return (frac * sigma1**2 + (1 - frac) * sigma2**2)**0.5

directory = f"fit_results/{variable}/"

# List of filenames and corresponding masses
filenames_masses = [
        ("500.txt", 500),
        ("1500.txt", 1500),
        ("2500.txt", 2500),
        ("3500.txt", 3500),
        ("4500.txt", 4500)
        ]

masses = []
combined_sigmas = []

for filename, mass in filenames_masses:
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        results = read_fit_results(filepath)
        
        frac = results['frac1']
        sigma1 = results['Sigma1']
        sigma2 = results['Sigma2']
        
        sigma_combined = compute_combined_sigma(frac, sigma1, sigma2)
        
        masses.append(mass)
        combined_sigmas.append(sigma_combined)
    else:
        print(f"File {filepath} not found.")

# Plot the combined sigma as a function of mass
plt.plot(masses, combined_sigmas, marker='o')
plt.xlabel('Higgs Mass [MeV]')
plt.ylabel('Combined Sigma [MeV]')
plt.title(f'Width vs Mass {variable}')
plt.grid(True)
plt.savefig(f'plots/{variable}/sigma_vs_mass{variable}.png')
plt.show()
# %%

# %%

