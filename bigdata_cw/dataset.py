import os
import requests
from pathlib import Path
import gzip
import shutil

# Configuration for URLs and paths
DATA_URLS = {
    "name.basics": "https://datasets.imdbws.com/name.basics.tsv.gz",
    "title.basics": "https://datasets.imdbws.com/title.basics.tsv.gz",
    "title.ratings": "https://datasets.imdbws.com/title.ratings.tsv.gz",
}
RAW_DATA_DIR = Path(__file__).resolve().parents[1] / 'data' / 'raw'


def download_data(url, dest_path):
    """
    Downloads a file from the given URL to the destination path.

    Args:
        url (str): The URL of the file to download.
        dest_path (Path): The destination path where the file will be saved.
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded: {dest_path.name}")
    else:
        print(f"Failed to download from {url}. Status code: {response.status_code}")


def download_all_datasets():
    """
    Downloads all IMDb datasets listed in DATA_URLS.
    """
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name, url in DATA_URLS.items():
        dest_path = RAW_DATA_DIR / f"{name}.tsv.gz"
        download_data(url, dest_path)


def extract_gz_files():
    """
    Extracts all .gz files in the raw data directory.
    """
    for file_path in RAW_DATA_DIR.glob("*.gz"):
        extracted_path = file_path.with_suffix('')
        with gzip.open(file_path, 'rb') as f_in:
            with open(extracted_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"Extracted: {extracted_path.name}")


if __name__ == "__main__":
    download_all_datasets()
    extract_gz_files()