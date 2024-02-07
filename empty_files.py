import os

def find_empty_files(folder_path):
    empty_files = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        # Check if it's a file and not a directory
        if os.path.isfile(file_path):
            # Check if file is empty
            if os.path.getsize(file_path) == 0:
                os.remove(file_path)
                empty_files.append(file)
    return empty_files

# Example usage
folder_path = 'captions/'
print(find_empty_files(folder_path))
