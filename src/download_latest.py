#!/usr/bin/env python
"""
Download the latest version of the BBGA source stuff.
"""

import shutil

import requests

METADATA_URL = 'https://api.data.amsterdam.nl/dcatd/datasets/G5JpqNbhweXZSw'


def download():
    print("Downloading metadata from", METADATA_URL)
    metadata_res = requests.get(METADATA_URL)
    metadata_res.raise_for_status()

    metadata = metadata_res.json()
    files = {
        '_:d2': '/app/data/bbga.csv',
        '_:d3': '/app/data/metadata.csv'
    }
    for dist in metadata['dcat:distribution']:
        if dist['@id'] in files:
            download_csv(dist['dcat:accessURL'], files[dist['@id']])

def download_csv(csv_location, target):
    print("Downloading CSV from", csv_location)
    csvfile = requests.get(csv_location, stream=True)
    csvfile.raise_for_status()
    with open(target, 'wb') as f:
        csvfile.raw.decode_content = True
        shutil.copyfileobj(csvfile.raw, f)
    print("Downloaded as", target)


if __name__ == "__main__":
    download()
