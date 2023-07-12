# SkullStrip_ANTsPyNet

Stand alone script to perform brain extraction using U-net and ANTs-based training data. From https://github.com/ANTsX/ANTsPyNet/blob/master/antspynet/utilities/brain_extraction.py

## Setup

```
pip install antspyx
pip install antspynet
```

## Usage

Usage: python3 script.py T1w.nii.gz Output_prefix

## Example:

```
python3 ~/Scripts/SkullStrip_ANTsPyNet/skullstrip_antspynet.py T1w.nii.gz brain
```
