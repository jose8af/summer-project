import uproot
import pandas as pd
import matplotlib.pyplot as plt

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

# Plotting the data
for i, dfs in dataframes.items():
    for directory, df in dfs.items():
        for leaf in leaves:
            plt.figure()
            plt.hist(df[leaf], bins='auto', alpha=0.7, range=[0, 7000 if i == 1 else 6100])
            plt.xlabel(leaf)
            plt.ylabel('Frequency')
            plt.title(f'Histogram of {leaf} in {directory} ({i+1})')
            plt.savefig(f'{leaf}_{i+1}.png')

