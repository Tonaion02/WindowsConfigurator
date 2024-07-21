#!/usr/bin/env python
import subprocess
import os
import shutil

from pathlib import Path
import requests





#===================================================================================================================
# DIRECTORIES_NAME class
# Build all the paths
class DIRECTORIES_NAME:

    # Change these names if you want to change directories' name
    _GARBAGE_DIR = "garbage"
    _DOWNLOADS_DIR = "downloadsTmp"
    _BASE_DIR = ""
    # Change these names if you want to change directories' name

    # Don't touch this, PRIVATE
    _debug = True
    _slash = "/"



    @staticmethod
    def _init():
        if DIRECTORIES_NAME._debug:
            DIRECTORIES_NAME._BASE_DIR = DIRECTORIES_NAME._GARBAGE_DIR

    @staticmethod
    def _get_garbage_dir():
        return DIRECTORIES_NAME._GARBAGE_DIR
    
    @staticmethod
    def _get_downloads_dir():
        # return DIRECTORIES_NAME._BASE_DIR + DIRECTORIES_NAME._slash + DIRECTORIES_NAME._DOWNLOADS_DIR
        return os.path.join(DIRECTORIES_NAME._BASE_DIR, DIRECTORIES_NAME._DOWNLOADS_DIR)
    # Don't touch this, PRIVATE


# Don't touch this, PRIVATE
DIRECTORIES_NAME._init()
GARBAGE_DIR = DIRECTORIES_NAME._get_garbage_dir()
DOWNLOADS_DIR = DIRECTORIES_NAME._get_downloads_dir()
BASE_DIR = DIRECTORIES_NAME._get_downloads_dir()
# Don't touch this, PRIVATE
#===================================================================================================================





def install_software(url: str, outfile, installation_directory=None):
    R = requests.get(url, allow_redirects=True)
    if R.status_code != 200:
        raise ConnectionError('could not download {}\nerror code: {}'.format(url, R.status_code))
    
    outfile = os.path.join(DOWNLOADS_DIR, outfile)
    pathOutFile = Path(outfile)
    pathOutFile.write_bytes(R.content)

    if installation_directory == None:
        print("Da fare!!!")
    else:
        subprocess.Popen(outfile + " /InstallDirectoryPath=[\"C:/test/firefox\"]", shell=True)





def create_base_directories():
    # Create garbage directory for garbage with name GARBAGE_DIR
    os.mkdir(GARBAGE_DIR)

    # Create downloads directory for downloads with name DOWNLOADS_DIR
    os.mkdir(DOWNLOADS_DIR)





if __name__ == "__main__":

    # TEMPORARY
    os.chdir("C:/source/Python/windows-configurator")

    # Cleaning
    shutil.rmtree("garbage", ignore_errors=True)

    create_base_directories()

    install_software("https://download.mozilla.org/?product=firefox-stub&os=win&lang=it", "firefox-installer.exe", "abla")