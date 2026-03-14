import urllib.request
import zipfile
import os
import stat
import tempfile
from xinstaller.common import *
from xinstaller.recipes import *
import shutil


def install_sv2v(prefix: str, version: str = "v0.0.12") -> None:
    url = f"https://github.com/zachjs/sv2v/releases/download/{version}/sv2v-Linux.zip"
    bin_dir = os.path.join(prefix, "bin")
    dest = os.path.join(bin_dir, "sv2v")

    os.makedirs(bin_dir, exist_ok=True)

    print(f"Downloading sv2v {version}...")
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = os.path.join(tmp, "sv2v.zip")

        urllib.request.urlretrieve(url, zip_path)

        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(tmp)

        binary = os.path.join(tmp, "sv2v-Linux", "sv2v")
        shutil.copy2(binary, dest)


    # Make executable
    st = os.stat(dest)
    os.chmod(dest, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    print(f"sv2v installed at {dest}")
    
    
