#!/bin/python3

import os
import json

def directory_to_json(path):
    """Converts a directory to a JSON object."""

    # Check if path is a directory
    if not os.path.isdir(path):
        raise ValueError(f"Path {path} is not a directory.")

    # Get all files in directory
    files = os.listdir(path)

    # Remove hidden files
    files = [file for file in files if not file.startswith(".")]

    # Create JSON object
    json_object = {}

    # Iterate over files
    for file in files:
        # Get file path
        file_path = os.path.join(path, file)

        # Check if file is a directory
        if os.path.isdir(file_path):
            # Recursively call directory_to_json
            json_object[file] = directory_to_json(file_path)
        else:
            # Read file content
            with open(file_path, "r") as f:
                content = f.read()

            # Add file content to JSON object
            json_object[file] = content

    return json_object

if __name__ == "__main__":
    # Convert directory to JSON object
    json_object = directory_to_json(".")

    # Dump JSON object to file
    with open("directory.json", "w") as f:
        json.dump(json_object, f, indent=4)