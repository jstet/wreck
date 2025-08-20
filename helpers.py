import requests
import tempfile
import zipfile
import os

def download_unzip(url, local_path):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192):
                temp_file.write(chunk)
        temp_file_path = temp_file.name

    os.makedirs(local_path, exist_ok=True)

    with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
        zip_ref.extractall(local_path)

    tsv_files = [f for f in os.listdir(local_path) if f.endswith('.txt')]
    if not tsv_files:
        raise FileNotFoundError("No .txt file found in the zip archive")

    return os.path.join(local_path, tsv_files[0])
