#!/usr/bin/env python3
"""
Script to fix deprecated Keras imports in Jupyter notebook.
Replaces old keras.* imports with tensorflow.keras.* imports.
"""

import json
import sys

def fix_keras_imports(notebook_path):
    """Fix Keras imports in a Jupyter notebook."""
    
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Define the replacements
    replacements = {
        'from keras.preprocessing.text import': 'from tensorflow.keras.preprocessing.text import',
        'from keras.preprocessing.sequence import': 'from tensorflow.keras.preprocessing.sequence import',
        'from keras.models import': 'from tensorflow.keras.models import',
        'from keras.layers import': 'from tensorflow.keras.layers import',
        'from keras.': 'from tensorflow.keras.',
        'import keras.': 'import tensorflow.keras.',
    }
    
    modified = False
    
    # Process each cell
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            source = cell['source']
            if isinstance(source, list):
                new_source = []
                for line in source:
                    original_line = line
                    for old, new in replacements.items():
                        if old in line:
                            line = line.replace(old, new)
                            if line != original_line:
                                modified = True
                                print(f"Fixed: {original_line.strip()} -> {line.strip()}")
                    new_source.append(line)
                cell['source'] = new_source
            elif isinstance(source, str):
                original_source = source
                for old, new in replacements.items():
                    if old in source:
                        source = source.replace(old, new)
                        if source != original_source:
                            modified = True
                cell['source'] = source
    
    if modified:
        # Write back the notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
        print(f"\n✓ Successfully updated {notebook_path}")
        print("Please restart your Jupyter kernel and re-run the cells.")
    else:
        print("No Keras imports found to fix.")
    
    return modified

if __name__ == "__main__":
    notebook_path = "/Users/amitrajpurkar/workspace/pyprojects/restaurant-eda/src/zomato-complete-eda-and-lstm-model.ipynb"
    
    if len(sys.argv) > 1:
        notebook_path = sys.argv[1]
    
    print(f"Fixing Keras imports in: {notebook_path}\n")
    fix_keras_imports(notebook_path)
