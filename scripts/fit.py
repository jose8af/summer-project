import uproot
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

# Paths to the ROOT files
root_file_paths = ["tuples/2500_3_dtf.root", "tuples/3500_3_dtf.root"]

# Directories and the tree name
directories = ["B"]
tree_name = "Tuple"
leaves = ["H_MASS"]

# Create a dictionary to store the dataframes for each ROOT file
dataframes = {}

# Function to extract data from a ROOT file
def extract_data(file_path, directories, tree_name, leaves):
    file = uproot.open(file_path)
    dfs = {}
    for directory in directories:
        tree = file[f"{directory}/{tree_name}"]
        data = {leaf: tree[leaf].array(library="np") for leaf in leaves}
        dfs[directory] = pd.DataFrame(data)
    return dfs

# Extract data from each ROOT file
for i, root_file_path in enumerate(root_file_paths):
    dataframes[i] = extract_data(root_file_path, directories, tree_name, leaves)

# Function to plot histogram with Gaussian fit
def plot_histogram_with_gaussian_fit(df, leaf, plot_range, filename_suffix):
    plt.figure()
    
    # Plot histogram
    counts, bins, _ = plt.hist(df[leaf], bins='auto', alpha=0.7, range=plot_range, density=True)
    
    # Fit Gaussian
    mu, std = norm.fit(df[leaf])
    
    # Plot Gaussian fit
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    
    # Labels and title
    plt.xlabel(leaf)
    plt.ylabel('Density')
    plt.title(f'Histogram of {leaf} with Gaussian fit')
    
    # Save the plot
    plt.savefig(f'{leaf}_{filename_suffix}.png')
    plt.close()

# Plotting the data with Gaussian fit
for i, dfs in dataframes.items():
    for directory, df in dfs.items():
        for leaf in leaves:
            plot_range = [0, 7000] if i == 1 else [0, 6100]
            plot_histogram_with_gaussian_fit(df, leaf, plot_range, f'{directory}_{i+1}')

