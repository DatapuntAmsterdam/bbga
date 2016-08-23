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
	zipfile_location = metadata['result']['resources'][0]['url']

	print("Downloading BBGA zip from", zipfile_location)
	zipfile = requests.get(zipfile_location, stream=True)
	zipfile.raise_for_status()

	with open('bbga.zip', 'wb') as f:
		zipfile.raw.decode_content = True
		shutil.copyfileobj(zipfile.raw, f)

	print("Downloaded as", "bbga.zip")



if __name__ == "__main__":
	download()
