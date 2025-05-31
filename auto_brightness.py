import os
import tkinter as tk
from tkinter import filedialog
import tifffile as tiff
import numpy as np
from tqdm import tqdm


root = tk.Tk()
root.withdraw()

selected_folder = filedialog.askdirectory()

file_paths = []

for root_dir, dirs, files in os.walk(selected_folder):
    for file in files:
        if file.lower().endswith('.tif') and 'enhanced' not in file.lower():
            file_paths.append(os.path.join(root_dir, file))

total_num = len(file_paths)

cnt = 0
for file in tqdm(file_paths):
    cnt += 1
    # tqdm.write(f'Proseeing {os.path.basename(file)} : {cnt}/{total_num}')

    output_file = f'{os.path.splitext(file)[0]}_enhanced.tif'
    im = tiff.imread(file)
    hist, bins = np.histogram(im, 255)

    threshold = im.size / 5000

    num_pix = 0
    min_im = 0
    max_im = im.max()

    for i in range(255):
        num_pix += hist[i]
        if num_pix > threshold:
            min_im = bins[i]
            break

    num_pix = 0
    for j in range(1, 255):
        num_pix += hist[-j]
        if num_pix > threshold:
            max_im = bins[-j]
            break
    
    fp = np.zeros(bins.shape)
    fp[:i] = 1
    fp[-j:] = 255
    for index in range(i, 256 - j):
        range_ = 256 - j - i
        step = 254 / range_
        fp[index] = (index - i) * step + 1

    im2 = np.interp(im.flatten(), bins, fp).reshape(im.shape).astype(np.uint8)
    tiff.imwrite(output_file, im2)