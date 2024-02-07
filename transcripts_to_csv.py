import os
import pandas as pd

def text_files_to_csv(folder_path, csv_file_path):
    # Initialize a list to hold file names and contents
    data = []

    # Walk through the folder to find text files
    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            youtube_id = file[11:-4]
            file_path = os.path.join(folder_path, file)
            
            # Read the contents of the file
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Append the youtube id and content to the list
            data.append([youtube_id, content])

    # Create a DataFrame from the list
    df = pd.DataFrame(data, columns=['Youtube ID', 'Content'])

    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)

    return f"CSV file created at: {csv_file_path}"

# Example usage
folder_path = 'captions/processed/'  # Replace with the actual folder path
csv_file_path = 'transcripts_11_01_24.csv'  # Replace with the desired CSV file path

# Call the function with the example paths
text_files_to_csv(folder_path, csv_file_path)  # Uncomment to use in a real scenario

