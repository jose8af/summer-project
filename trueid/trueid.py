import ROOT
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


rootfile = f'../tuples/minbias_tuple.root'
file = ROOT.TFile.Open(rootfile) 
mintuple = file['B/Tuple']

mpid = []
mmid = []

pdg_map = {
    11: "Electron (e⁻)",
    -11: "Positron (e⁺)",
    13: "Muon (μ⁻)",
    -13: "Anti-muon (μ⁺)",
    0: "Undefined (?)",
    211: "Pion (π⁺)",
    -211: "Anti-pion (π⁻)",
    2212: "Proton (p)"
}

for value in mintuple:
    mu_plus_id = int(value.GetLeaf('mu_plus_TRUEID').GetValue())
    mu_minus_id = int(value.GetLeaf("mu_minus_TRUEID").GetValue())
    
    mpid.append(pdg_map.get(mu_plus_id, "Unknown"))
    mmid.append(pdg_map.get(mu_minus_id, "Unknown"))


# %%
mpid
# %%
all_particles = mpid + mmid

particle_counts = Counter(all_particles)

total_particles = sum(particle_counts.values())

particle_percentages = {particle: (count / total_particles) * 100 for particle, count in particle_counts.items()}

# %%

# Sort particles by percentage for a better visual representation
sorted_particles = sorted(particle_percentages.items(), key=lambda x: x[1], reverse=True)

# Unpack the sorted items for plotting
particles, percentages = zip(*sorted_particles)

# Plotting the pie chart
plt.figure(figsize=(8, 8))
plt.pie(percentages, labels=particles, autopct='%1.1f%%', colors=plt.cm.Paired.colors)
plt.title('Particle Type Distribution')
plt.savefig('mu_trueID.png')
plt.show()

# %%
particle_counts.values()
# %%
total_particles
# %%
particle_percentages
# %%

