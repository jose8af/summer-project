import ROOT
import os
import numpy as np
import matplotlib.pyplot as plt

def perform_fit(energy, variable, value1, value2):
    ini_range = energy - value1
    fin_range = energy + value2

    rootfile = f'../tuples/{energy}_3ns_tuple.root'
    file = ROOT.TFile.Open(rootfile)
    filetuple = file['B']
    df = ROOT.RDataFrame('Tuple', filetuple)

    x = ROOT.RooRealVar('x', 'mass observable', ini_range, fin_range)
    roo_data_set_hmass = df.Book(ROOT.std.move(ROOT.RooDataSetHelper('dataset', variable, ROOT.RooArgSet(x))), ([variable]))
    data = roo_data_set_hmass.GetValue()

    mu = ROOT.RooRealVar("mu", "mu", energy, energy - 3, energy + 3)
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

    # Plot the fit result
    c = ROOT.TCanvas('crystal', 'crystal', 800, 600)
    xframe = x.frame(ROOT.RooFit.Range(ini_range, fin_range))
    xframe.SetTitle(f'{energy} {variable} Double Crystal Ball Fit')
    data.plotOn(xframe, ROOT.RooFit.Binning(150))
    model.plotOn(xframe)
    model.paramOn(xframe, ROOT.RooFit.Layout(0.6, 0.9, 0.9))
    xframe.Draw()
    os.makedirs(f'plots/{variable}', exist_ok=True)
    c.SaveAs(f'plots/{variable}/{energy}.png')

    # Save fit results
    os.makedirs(f'fit_results/{variable}', exist_ok=True)
    with open(f"fit_results/{variable}/{energy}.txt", "w") as f:
        f.write(f"frac1: {frac_crystal.getVal()} ± {frac_crystal.getError()}\n")
        f.write(f"mu: {mu.getVal()} ± {mu.getError()}\n")
        f.write(f"Sigma1: {sigma.getVal()} ± {sigma.getError()}\n")
        f.write(f"Sigma2: {sigma2.getVal()} ± {sigma2.getError()}\n")
        f.write(f"alpha1: {alpha.getVal()} ± {alpha.getError()}\n")
        f.write(f"alpha2: {alpha2.getVal()} ± {alpha2.getError()}\n")
        f.write(f"n: {n.getVal()} ± {n.getError()}\n")
        f.write(f"n2: {n2.getVal()} ± {n2.getError()}\n")

    # Plot the pull distribution
    pull_frame = x.frame()
    pull_frame.SetTitle(f"Pull Dist. Double Cryst {energy}")
    pull_hist = xframe.pullHist()
    pull_frame.addPlotable(pull_hist, "P")

    c2 = ROOT.TCanvas("c2", "Pull Distribution", 800, 600)
    pull_frame.Draw()
    c2.SaveAs(f'plots/{variable}/pull_{energy}.png')

# Function to read fit results from a file
def read_fit_results(filename):
    results = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.split(':')
            value, error = value.split('±')
            results[key.strip()] = (float(value.strip()), float(error.strip()))
    return results

# Function to compute combined sigma with uncertainty
def compute_combined_sigma(frac, sigma1, sigma2, frac_err, sigma1_err, sigma2_err):
    #sigma_combined = (frac**2 * sigma1**2 + (1 - frac)**2 * sigma2**2 + frac*(1-frac)*sigma1*sigma2)**(1/2)
    sigma_combined = (frac**2 * sigma1**2 + (1 - frac)**2 * sigma2**2)**(1/2)

    # Error propagation
    d_sigma_combined_d_frac = sigma1**2 + sigma2**2
    d_sigma_combined_d_sigma1 = 2*frac*sigma1
    d_sigma_combined_d_sigma2 = 2*sigma2*(1 - frac)

    sigma_combined_err = np.sqrt(
        (d_sigma_combined_d_frac * frac_err)**2 +
        (d_sigma_combined_d_sigma1 * sigma1_err)**2 +
        (d_sigma_combined_d_sigma2 * sigma2_err)**2
    )
    
    return sigma_combined, sigma_combined_err

def plot(masses, widths, variable):
    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.size'] = 16  
    plt.rcParams['legend.fontsize'] = 14  
    
    # Plotting the data points with a connecting line
    plt.plot(masses, widths, linestyle='None', color='blue', marker='s', markerfacecolor='red', markersize=8, label='Data Points')

    plt.xlabel(r'Higgs Mass [\textit{MeV}]')
    plt.ylabel(r'Width [\textit{MeV}]')
    plt.title(rf'Width vs Mass for {variable}')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='best')
    
    # Save the plot
    plt.savefig(f'plots/width_vs_mass/{variable}.png')
    plt.show()
