#!/usr/bin/env python
"""
Download the latest version of the BBGA source stuff.
"""

import requests
import shutil


METADATA_URL = 'http://data.amsterdam.nl/api/3/action/package_show?id=basisbestand-gebieden-amsterdam--bbga-'


def download():
	print("Downloading metadata from", METADATA_URL)
	metadata_res = requests.get(METADATA_URL)
	metadata_res.raise_for_status()

	metadata = metadata_res.json()
	download_csv(metadata['result']['resources'][1]['url'], 'bbga.csv')
	download_csv(metadata['result']['resources'][2]['url'], 'metadata.csv')

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
