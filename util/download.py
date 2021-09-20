import os
import requests
from tqdm import tqdm
import zipfile

def download_data(num_file=None):
    """
    Downloads training files from LUNA16
    https://luna16.grand-challenge.org/

    num_file: Optional[List, int]
        Specifiy which subset of data to download.
        Default is none, which will download all the subset from 0 to 9.
        To specifiy, use a list of int or int, 
        e.g: 
            num_file=1 will download subset 1
            num_file=[5, 8] will download subset 5 and 8
    """
    if num_file is None:
        num_file = [i for i in range(10)]

    if isinstance(num_file, int):
        num_file = [num_file]

    save_path = 'data-unversion/part2/luna/'

    for i in num_file:
        id = 3723295 if i <= 6 else 4121926
        link = f"https://zenodo.org/record/{id}/files/"
        url = link + f"subset{i}.zip"
        response = requests.get(url, stream=True)
        filename = url.split("/")[-1]
        with tqdm.wrapattr(open(save_path + filename, "wb"), "write",
                        miniters=1, desc=url.split('/')[-1],
                        total=int(response.headers.get('content-length', 0))) as fout:
            for chunk in response.iter_content(chunk_size=4096):
                fout.write(chunk)
            
        
        with zipfile.ZipFile(save_path + filename, 'r') as zip_ref:
            print(f"Extracting {filename} to {save_path + filename}")
            zip_ref.extractall(save_path + filename)
        
        if os.path.isfile(save_path + filename):
            print(f"Removing {filename}")
            os.remove(save_path + filename)
