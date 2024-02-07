#!/bin/bash

# Directory containing the .txt files
DIRECTORY='./captions/'

# Loop throutgh each .txt file in the directory
for FILE in "$DIRECTORY"/*.txt; do
    # Check if the file exists
    if [ -f "$FILE" ]; then
        # Change the file extension from .txt to .json
        mv "$FILE" "${FILE%.txt}.json"
    fi
done
