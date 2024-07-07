import uproot

# Path to the ROOT file
root_file_path = "tuples/2500_3_dtf.root"

# Directory and tree name
directory = "Higgs"
tree_name = "Tuple"

# Open the ROOT file
file = uproot.open(root_file_path)

# Access the specified tree
tree = file[f"{directory}/{tree_name}"]

# List all leaves (branches) in the tree
leaves = tree.keys()
print(f"Leaves in the '{directory}/{tree_name}' tree:")
for leaf in leaves:
    print(leaf)


