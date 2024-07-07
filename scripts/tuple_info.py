import uproot

# Path to the ROOT file
root_file_path = "tuples/3500_3_dtf.root"

# Open the ROOT file
file = uproot.open(root_file_path)

# Function to recursively explore the file structure
def explore_file_structure(directory, indent=0):
    for key, item in directory.items():
        print(" " * indent + key)
        if isinstance(item, uproot.models.TTree.Model_TTree):
            print(" " * (indent + 2) + "Branches:")
            for branch in item.keys():
                print(" " * (indent + 4) + branch)
        elif isinstance(item, uproot.reading.ReadOnlyDirectory):
            explore_file_structure(item, indent + 2)

# Explore the structure of the ROOT file
explore_file_structure(file)

