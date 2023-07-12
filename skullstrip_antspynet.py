import sys

if len(sys.argv) != 3:
    print("Usage: python3 script.py T1w.nii.gz Output_prefix")
    quit()

from antspynet import brain_extraction
import os
from ants import atropos, get_ants_data, image_read, resample_image, get_mask

import subprocess

value = sys.argv[1]
example_filename = os.path.join('.', value)
img = image_read(example_filename)

# Run the brain extraction from ANTsPyNet:
probability_brain_mask = brain_extraction(img, modality="t1")

prefix = sys.argv[2]
prefixmask = f"{prefix}_mask.nii.gz"
output_filename = os.path.join('.', prefixmask)

probability_brain_mask.to_file(output_filename)

antsorig_filename = os.path.join('.', f"{prefix}.nii.gz")

subprocess.run(["flirt", "-in", f"{output_filename}", "-ref", f"{sys.argv[1]}", "-out", f"{output_filename}", "-applyxfm", "-usesqform"])
subprocess.run(["fslmaths", f"{output_filename}", "-thr", "0.5", "-bin", f"{output_filename}"])
subprocess.run(["fslmaths", f"{output_filename}", "-mul", sys.argv[1], f"{antsorig_filename}"])