import ROOT
import numpy as np
from functions.functions import plot

# List of variables and energies
b_variables = ['H_DTF_BestPV_MASS', 'H_DTF_noConstraint_MASS', 'H_DTF_BestPVOnly_MASS', 'H_DTF_noPV_MASS']
h_variables = ['H_DTF_noConstraint_Higgs_MASS', 'H_DTF_BestPV_Higgs_MASS']
energies = [500, 1500, 2500, 3500, 4500]
def calculate_width(variable_array):
    
    percent_left = np.percentile(variable_array, 15.8)
    percent_right = np.percentile(variable_array, 84.1)
    central_value = (percent_right - percent_left) / 2
    return central_value

for var in h_variables:
    path = f'plots/width_vs_mass/trueend/{var}_l5000.png'
    masses = []
    widths = [] 
    for energy in energies:
        rootfile = f'../tuples/{energy}_3ns_tuple.root'
        file = ROOT.TFile.Open(rootfile)
        bsm_tuple = file['Higgs']
        df = ROOT.RDataFrame('Tuple', bsm_tuple)
        filter_out = df.Filter(f'{var} >= 0 && {var} <= {energy}*{energy} && H_TRUEEND_VZ  < 5000')

        tuple_array = filter_out.AsNumpy([var])
        variable_array = tuple_array[var]
        width = calculate_width(variable_array)
       
        masses.append(energy)
        widths.append(width)

    plot(masses, widths, var, path)

# %%

