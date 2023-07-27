#!/bin/python3

import os
import json

def directory_to_json(path):
    """Converts a directory to a JSON object."""

    # Check if path is a directory
    if not os.path.isdir(path):
        raise ValueError(f"Path {path} is not a directory.")
    
    print(f"Converting directory {os.path.abspath(path)} to JSON object.")

    # Get all files in directory
    elements = os.listdir(path)

    # Remove hidden files
    elements = [file for file in elements if not file.startswith(".")]
    directories = [file for file in elements if os.path.isdir(os.path.join(path, file))]
    files = [file for file in elements if os.path.isfile(os.path.join(path, file))]

    if not len(directories) > 0:
        return files

    # Create JSON object
    json_object = {}

    # Add directories to JSON object
    for directory in directories:
        json_object[directory] = directory_to_json(os.path.join(path, directory))

    if files:
        json_object["files"] = files

    return json_object

if __name__ == "__main__":
    # Convert directory to JSON object
    json_object = directory_to_json(".")

    # Dump JSON object to file
    with open("directory.json", "w") as f:
        json.dump(json_object, f, indent=4)