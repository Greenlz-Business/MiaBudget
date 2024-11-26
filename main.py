# File created by GreenLz
# MiaBudget was made from a quick spaghetti script called Closed-GLZ-Bugdet
# It is a saucepan full of Youtube tutorials, Chatgpt poop, great forums and own intuition
# It helped me to learn python and the github environment with version tracking
# Project started on 19-Nov-2024
__version__ = "0.1.0"

import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative paths to the target scripts
converter = os.path.join(current_dir, "converter", "transaction_processor.py")
extractor = os.path.join(current_dir, "processor", "extractor.py")
pdfer = os.path.join(current_dir, "crafter", "pdfer.py")

# Execute the target scripts
with open(converter, 'r') as f:
    exec(f.read())
with open(extractor, 'r') as f:
    exec(f.read())
with open(pdfer, 'r') as f:
    exec(f.read())
