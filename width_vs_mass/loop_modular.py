import os
import matplotlib.pyplot as plt
from code.functions import perform_fit, read_fit_results, compute_combined_sigma

energies = [500, 1500, 2500, 3500, 4500]
variable = 'H_M' #H_DTF_BestPVOnly_MASS  H_M H_DTF_BestPV_MASS

l_limit = 800
r_limit = 1000
for energy in energies:
    perform_fit(energy, variable, l_limit, r_limit)

directory = f"fit_results/{variable}/"
masses = []
combined_sigmas = []
combined_sigmas_err = []

output_file = f'error_values/{variable}_sigma_combined_results.txt'

with open(output_file, 'w') as f: 
    f.write('Energy [MeV]\tSigma Combined [MeV]\tSigma Combined Error [MeV]\n')

    for energy in energies:
        filepath = os.path.join(directory, f"{energy}.txt")
        if os.path.exists(filepath):
            results = read_fit_results(filepath)

            frac, frac_err = results['frac1']
            sigma1, sigma1_err = results['Sigma1']
            sigma2, sigma2_err = results['Sigma2']

            sigma_combined, sigma_combined_err = compute_combined_sigma(
                frac, sigma1, sigma2, frac_err, sigma1_err, sigma2_err
            )

            masses.append(energy)
            combined_sigmas.append(sigma_combined)
            combined_sigmas_err.append(sigma_combined_err)
            
            f.write(f'{energy}\t{sigma_combined:.6f}\t{sigma_combined_err:.6f}\n')

        else:
            print(f"File {filepath} not found.")



plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 16  
plt.rcParams['legend.fontsize'] = 14  
plt.errorbar(masses, combined_sigmas, yerr=combined_sigmas_err, fmt='s', capsize=5, color='blue', markerfacecolor='red', markersize=8, label='Data Points')

plt.plot(masses, combined_sigmas, linestyle='-', color='gray', alpha=0.6)
plt.xlabel(r'Higgs Mass [\textit{MeV}]')
plt.ylabel(r'Combined Sigma [\textit{MeV}$^{2}$]')
plt.title(rf'Width vs Mass for {variable}')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='best')
plt.savefig(f'plots/{variable}/sigma_vs_mass_{variable}.png')
plt.show()

