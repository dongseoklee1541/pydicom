from __future__ import print_function

import tempfile

import pydicom
from pydicom.data import get_testdata_files

print(__doc__)

# Anonymize a single file
filename = get_testdata_files('MR_small.dcm')[0]
dataset = pydicom.dcmread(filename)

data_elements = ['PatientID',
                 'PatientBirthDate']

for de in data_elements:
    print(dataset.data_element(de))


def person_names_callback(dataset, data_element):
    if data_element.VR == "PN":
        data_element.value = "anonymous"


def curves_callback(dataset, data_element):
    if data_element.tag.group & 0xFF00 == 0x5000:
        del dataset[data_element.tag]


dataset.PaitentID = "id"
dataset.walk(person_names_callback)
dataset.walk(curves_callback)

dataset.remove_private_tags() # remove private tag

# Data element of type 3 (optional) can be easily deleted using del or delattr.
if 'OtherPatientIDs' in dataset:
    delattr(dataset, 'OtherPatientIDs')

if 'OtherPatientIDsSequence' in dataset:
    del dataset.OtherPatientIDsSequence

# For data elements of type 2, this is possible to blank it by assigning a blank string.
tag = 'PatientBirthDate'
if tag in dataset:
    dataset.data_element(tag).value = '19000101'

# Finally, this is possible to store the image

data_elements = ['PatientID',
                 'PatientBirthDate']

for de in data_elements:
    print(dataset.data_element(de))

output_filename = tempfile.NamedTemporaryFile().name
dataset.save_as(output_filename)