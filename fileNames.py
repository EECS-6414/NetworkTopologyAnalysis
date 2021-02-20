from os import listdir

# Function to return all file pathways and their corresponding file names
def files(mainPath):

    # List all folder names in the main pathway
    folderPath = [f for f in listdir(mainPath)]

    # Create a blank array
    return folderPath