"""
Created on Mon Oct 12 15:14:14 2020

@author: mtb
"""

import re
import requests
from bs4 import BeautifulSoup
import os


def find_file_address(base_url, reg_pattern):
    """Given a base url address, find all the html links on the page that match a certain regex pattern and return them
     in a list"""
    req = requests.get(base_url)
    soup = BeautifulSoup(req.text, "lxml")
    pages = soup.findAll("a", href=re.compile(reg_pattern))
    return pages


def download_file(url):
    """Given a url address, the function downloads the file and save it in the current location with the name being
    the last 3 parts of the url """

    path = "ex1_download/"+"".join(url.split("/")[-3:])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, "wb") as f:
            for chunk in r:
                f.write(chunk)


def main():
    host = "https://www.football-data.co.uk/"
    base_url = host + "englandm.php"
    reg_pattern = "^mmz"
    pages = find_file_address(base_url, reg_pattern)

    for page in pages:
        url = host + page.get("href")
        download_file(url)


if __name__ == "__main__":
    main()
