import hashlib
import os
import requests
from tqdm import tqdm
import zipfile


MD5 = {
    "subset0.zip": "1065b0f42b8c25cf29260fd924a3c3a2",
    "subset1.zip": "2eda28bb123543074f5cd849499b87ff",
    "subset2.zip": "685b484b085bcdb81c525f3b1bf97c51",
    "subset3.zip": "54707e9e8954af29326eed60f38ea321",
    "subset4.zip": "98225ccb1a41fc434631f63f4284796a",
    "subset5.zip": "395ec714c4123cf213fb7b08f05ee9cc",
    "subset6.zip": "d162df1444a6f2674ab8273c7f9e1520",
    "subset7.zip": "e99b8921990d1414bb5e92130371e8a3",
    "subset8.zip": "38260ca9a8741888997bcebedfabc3f1",
    "subset9.zip": "e55c473bbeebd712eb2224a58998be8e",
}

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def download_data(num_file=None):
    """
    Downloads training files from LUNA16
    https://luna16.grand-challenge.org/

    num_file: Optional[List, int]
        Specifiy which subset .zipof data to download.
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
        response = requests.get(url + "?download=1", stream=True)
        filename = url.split("/")[-1]

        if os.path.isfile(save_path + filename):
            print(f"File {filename} already existed, skipping download")
        else:
            with tqdm.wrapattr(open(save_path + filename, "wb"), "write",
                            miniters=1, desc=url.split('/')[-1],
                            total=int(response.headers.get('content-length', 0))) as fout:
                for chunk in response.iter_content(chunk_size=4096):
                    fout.write(chunk)
        current_md5 = md5(save_path + filename)
        # assert current_md5 == MD5[filename], "MD5 mismatched, file corrupted"
            
        print(f"Extracting {filename} to {save_path + filename}")
        with zipfile.ZipFile(save_path + filename, 'r') as zip_ref:
            zip_ref.extractall(save_path + filename)
        
        print(f"Removing {filename}")
        os.remove(save_path + filename)


if __name__ == "__main__":
    download_data(0)
