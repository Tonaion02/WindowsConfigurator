#!/usr/bin/env python
import subprocess
import os
import shutil

from pathlib import Path
import requests

import xml.etree.ElementTree as ET





#===================================================================================================================
# ------------------------------------------------------------------------------------------------------------------
# DIRECTORIES_NAME class TODO: change with an appropriate name
# Builds and contains all the paths necessary for the program
# TODO: necessary to understand what to do where i am not in debug mode with the BASE_DIR
# what directory become the BASE_DIR?
# ------------------------------------------------------------------------------------------------------------------
class DIRECTORIES_NAME:

    # Change these names if you want to change directories' name (START)
    _GARBAGE_DIR = "garbage"
    _DOWNLOADS_DIR = "downloadsTmp"
    _TO_MANUALLY_INSTALL_DIR = "toManuallyInstall"
    _BASE_DIR = ""
    # Change these names if you want to change directories' name (END)

    # Don't touch this, PRIVATE (START)
    _debug = True



    @staticmethod
    def _init():
        if DIRECTORIES_NAME._debug:
            DIRECTORIES_NAME._BASE_DIR = DIRECTORIES_NAME._GARBAGE_DIR
        else:
            pass # SYSTEM_BASE_DIR

    @staticmethod
    def _get_garbage_dir():
        return DIRECTORIES_NAME._GARBAGE_DIR
    
    @staticmethod
    def _get_downloads_dir():
        return os.path.join(DIRECTORIES_NAME._BASE_DIR, DIRECTORIES_NAME._DOWNLOADS_DIR)
    
    @staticmethod
    def _get_to_manually_install_dir():
        return os.path.join(DIRECTORIES_NAME._BASE_DIR, DIRECTORIES_NAME._TO_MANUALLY_INSTALL_DIR)
    # Don't touch this, PRIVATE (END)


# Don't touch this, PRIVATE (START)
DIRECTORIES_NAME._init()
GARBAGE_DIR = DIRECTORIES_NAME._get_garbage_dir()
DOWNLOADS_DIR = DIRECTORIES_NAME._get_downloads_dir()
BASE_DIR = DIRECTORIES_NAME._get_downloads_dir()
TO_MANUALLY_INSTALL_DIR = DIRECTORIES_NAME._get_to_manually_install_dir()
# Don't touch this, PRIVATE (END)
#===================================================================================================================





#===================================================================================================================
#-------------------------------------------------------------------------------------------------------------------
# OUTPUT_FORMATTER Class
# This class contains methods to print on the command line output for debug purpose
#-------------------------------------------------------------------------------------------------------------------
class OUTPUT_FORMATTER:

    @staticmethod
    def print_logo():
        print("+===================================================================================================================+")
        print("+                                          WINDOWS-CONFIGURATOR                                                     +")
        print("+===================================================================================================================+")

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
        # subprocess.Popen(outfile + "/S /InstallDirectoryPath=\"C:/test/firefox\"", shell=True)
        res = os.system("choco.exe ")
        print(res)





def create_base_directories():
    # Create garbage directory for garbage with name GARBAGE_DIR
    os.mkdir(GARBAGE_DIR)

    # Create downloads directory for downloads with name DOWNLOADS_DIR
    os.mkdir(DOWNLOADS_DIR)

    # Create manually install directories
    os.mkdir(TO_MANUALLY_INSTALL_DIR)





# Modify or create an enviroment variable PERMANENTLY
# PERMANENTLY means that the changes are not local to this shell
# It already adds " to value to support spaces in value
def setX(name: str, value: str) -> None:
    os.system("SETX " + name + " \"" + value + "\"")




# TEMP
def testParseXml(name: str) -> None:

    class BackupPath:
        def __init__(self, path: str):
            self.intern = path

        def __str__(self):
            return "BackupPath: " + str(self.intern)
        
    def print_element(e):
        if type(e) is BackupPath:
            print(str(e))
            
        elif type(e) is ET.Element:
            print("Element: " + e.tag + " name: " + str(e.attrib) + " childs number: " + str(len(list(e))))

    # Variable that mantain the path of the current working directory like a string
    actualPath = BASE_DIR

    # Starting to parse file and retrieve root element
    tree = ET.parse(name)
    root = tree.getroot()

    # Use list like a stack with append and pop
    stackElements = []
    stackElements.append(root)

    while len(stackElements) > 0:

        # DEBUG
        print("\n StackElements:")
        for element in stackElements:
            print_element(element)
        print("StackElements end")
        
        # Pop the last element
        poppedElement = stackElements.pop(len(stackElements) - 1)

        # Check if the last element is a BackupPath or an Element of the tree (START)
        if type(poppedElement) is BackupPath:
            # DEBUG
            print(poppedElement)

            # TODO change effectevly the current working directory
            actualPath = poppedElement.intern
            continue
        elif type(poppedElement) is ET.Element:
            pass
        # Check if the last element is a BackupPath or an Element of the tree (END)

        if len(list(poppedElement)) > 0:
            stackElements.append(BackupPath(actualPath))

        # Retrieve all the child elements of the poppedElement and put in the stack
        for child in poppedElement:
            stackElements.append(child)

        # DEBUG
        print_element(poppedElement)

        


    
if __name__ == "__main__":

    OUTPUT_FORMATTER.print_logo()

    # # TEMP
    # # Testing changing enviroments' variables
    # os.system("SETX TEST_VARIABLE ciao")
    # t = os.getenv("PATH")
    # print("$TEST_VARIABLE: " + str(t))
    # os.system("SETX TEST_VARIABLE " + "\"" + t + "ciao" + "\"")

    # TEMP
    os.chdir("C:/source/Python/windows-configurator")

    # Cleaning
    shutil.rmtree("garbage", ignore_errors=True)

    create_base_directories()

    # install_software("https://download.mozilla.org/?product=firefox-stub&os=win&lang=it", "firefox-installer.exe", "abla")

    testParseXml("resources.xml")