import difflib

import pydicom
from pydicom.data import get_testdata_files
# get_test_data_files : Return test data files from pydicom data root.

print(__doc__)

filename_mr = get_testdata_files('MR_small.dcm')[0]
filename_ct = get_testdata_files('CT_small.dcm')[0]

datasets = tuple([pydicom.dcmread(filename, force=True)
                  for filename in (filename_mr, filename_ct)])

rep = []
for dataset in datasets:
    lines = str(dataset).split("\n")
    lines = [line + "\n" for line in lines]
    rep.append(lines)

diff = difflib.Differ()
for line in diff.compare(rep[0], rep[1]):
    if line[0] != "?":
        print(line)