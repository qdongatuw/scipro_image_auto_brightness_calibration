import os
import tkinter as tk
from tkinter import filedialog
import tifffile as tiff
import numpy as np


resolution = (6000000, 1000000)
unit = 5    # micrometer


def reset_resolution(path, resolution_x, resolution_y, unit=None):
    with tiff.TiffFile(path, mode='r+') as tif:
        _ = tif.pages[0].tags['XResolution'].overwrite(resolution_x)
        _ = tif.pages[0].tags['YResolution'].overwrite(resolution_y)
        if unit is not None:
            _ = tif.pages[0].tags['ResolutionUnit'].overwrite(unit)


root = tk.Tk()
root.withdraw()

selected_folder = filedialog.askdirectory()

file_paths = []

for root_dir, dirs, files in os.walk(selected_folder):
    for file in files:
        if file.lower().endswith('.tif'):
            file_paths.append(os.path.join(root_dir, file))

print(len(file_paths))
for file in file_paths:
    reset_resolution(file, resolution, resolution, unit)