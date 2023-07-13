import sys
import textwrap

if len(sys.argv) < 3:
    print("Usage: python3 script.py T1w.nii.gz Output_prefix [modality]")
    print("")
    print("Optional: modality: [default = t1]")
    print(textwrap.dedent("""Modality image type.  Options include:
    * "t1": T1-weighted MRI---ANTs-trained.  Previous versions are specified as "t1.v0", "t1.v1".
    * "t1nobrainer": T1-weighted MRI---FreeSurfer-trained: h/t Satra Ghosh and Jakub Kaczmarzyk.
    * "t1combined": Brian's combination of "t1" and "t1nobrainer".  One can also specify
                    "t1combined[X]" where X is the morphological radius.  X = 12 by default.
    * "flair": FLAIR MRI.   Previous versions are specified as "flair.v0".
    * "t2": T2 MRI.  Previous versions are specified as "t2.v0".
    * "t2star": T2Star MRI.
    * "bold": 3-D mean BOLD MRI.  Previous versions are specified as "bold.v0".
    * "fa": fractional anisotropy.  Previous versions are specified as "fa.v0".
    * "t1t2infant": Combined T1-w/T2-w infant MRI h/t Martin Styner.
    * "t1infant": T1-w infant MRI h/t Martin Styner.
    * "t2infant": T2-w infant MRI h/t Martin Styner.
    """))
    quit()

# Make sure this is installed on your python env:  pip install antspynet
from antspynet import brain_extraction
import os

#Make sure this is installed on your python env: pip install antspyx
from ants import atropos, get_ants_data, image_read, resample_image, get_mask

import subprocess

value = sys.argv[1]
example_filename = os.path.join('.', value)
img = image_read(example_filename)

# Check modality (or assume t1)
if len(sys.argv) == 4:
    modalityopt = sys.argv[3]
    print("")
    print("".join(["Using modality: ", f"{sys.argv[3]}"]))
else:
    modalityopt = "t1"
    print("")
    print("Assuming modality: t1")

# Run the brain extraction from ANTsPyNet:
probability_brain_mask = brain_extraction(img, modality=modalityopt)

prefix = sys.argv[2]
prefixmask = f"{prefix}_mask.nii.gz"
output_filename = os.path.join('.', prefixmask)

probability_brain_mask.to_file(output_filename)

antsorig_filename = os.path.join('.', f"{prefix}.nii.gz")

subprocess.run(["flirt", "-in", f"{output_filename}", "-ref", f"{sys.argv[1]}", "-out", f"{output_filename}", "-applyxfm", "-usesqform"])
subprocess.run(["fslmaths", f"{output_filename}", "-thr", "0.5", "-bin", f"{output_filename}"])
subprocess.run(["fslmaths", f"{output_filename}", "-mul", sys.argv[1], f"{antsorig_filename}"])