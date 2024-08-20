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
# TODO: necessary rebase all the paths from a full path
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
    def _init(path: str):
        if DIRECTORIES_NAME._debug:
            DIRECTORIES_NAME._BASE_DIR = os.path.join(path, DIRECTORIES_NAME._GARBAGE_DIR)
        else:
            pass # SYSTEM_BASE_DIR

    @staticmethod
    def _get_garbage_dir():
        return DIRECTORIES_NAME._GARBAGE_DIR
    
    @staticmethod
    def _get_base_dir():
        return DIRECTORIES_NAME._BASE_DIR

    @staticmethod
    def _get_downloads_dir():
        return os.path.join(DIRECTORIES_NAME._BASE_DIR, DIRECTORIES_NAME._DOWNLOADS_DIR)
    
    @staticmethod
    def _get_to_manually_install_dir():
        return os.path.join(DIRECTORIES_NAME._BASE_DIR, DIRECTORIES_NAME._TO_MANUALLY_INSTALL_DIR)
    # Don't touch this, PRIVATE (END)


# Don't touch this, PRIVATE (START)
DIRECTORIES_NAME._init("C:/source/Python/windows-configurator")
GARBAGE_DIR = DIRECTORIES_NAME._get_garbage_dir()
DOWNLOADS_DIR = DIRECTORIES_NAME._get_downloads_dir()
BASE_DIR = DIRECTORIES_NAME._get_base_dir()
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
        print("|                                          WINDOWS-CONFIGURATOR                                                     |")
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
        
    class TAGS:
        DIRECTORY = "directory"
        FILE = "file"
        SOFTWARE = "software"
        DATA = "data"
        CHOCO = "chocolatey-dependencies"
    
    class ATTRIB:
        NAME = "name"


    def print_element(e):
        if isinstance(e, Path): 
            print(str(e))
            
        elif type(e) is ET.Element:
            print("Element: " + e.tag + " name: " + str(e.attrib) + " childs number: " + str(len(list(e))))



    # Variable that mantain the path of the current working directory like a string
    cwd_path = BASE_DIR

    # Starting to parse file and retrieve root element
    tree = ET.parse(name)
    root = tree.getroot()

    # Use list like a stack with append and pop
    # Warning: we append and pop from the end of
    # the stack
    stack_elements = []
    stack_elements.append(root)

    # Change current working directory
    os.chdir(cwd_path)



    while len(stack_elements) > 0:

        # DEBUG
        print("\n StackElements:")
        for element in stack_elements:
            print_element(element)
        print("StackElements end")
        
        # Pop the last element
        popped_element = stack_elements.pop(len(stack_elements) - 1)

        # Check if the last element is a BackupPath or an Element of the tree (START)
        if isinstance(popped_element, BackupPath):
            # DEBUG
            print(popped_element)

            # TODO change effectevly the current working directory only if the current working directory
            # is different from the directory where we must be
            # TEMP(temporary solution that doesn't work properly)
            if cwd_path != popped_element.intern:
                cwd_path = popped_element.intern
                os.chdir(cwd_path)
            continue

        elif type(popped_element) is ET.Element:
            if popped_element.tag == TAGS.DIRECTORY:
                # If the directory "cwd_path\popped_element.attrib['name']" doesn't exist create it
                popped_element_dir_path = os.path.join(cwd_path, popped_element.attrib[ATTRIB.NAME])
                if not os.path.isdir(popped_element_dir_path):
                    os.mkdir(popped_element_dir_path)

                # if the directory isn't empty and we are in another directory, change directory
                # then save the current value of cwd_path in a BackupPath in a 
                if len(list(popped_element)) > 0:
                    stack_elements.append(BackupPath(cwd_path))
                    cwd_path = popped_element_dir_path
                    os.chdir(cwd_path)



            elif popped_element.tag == TAGS.FILE:
                pass
            elif popped_element.tag == TAGS.SOFTWARE:
                pass
            elif popped_element.tag == TAGS.DATA:
                pass
            elif popped_element.tag == TAGS.CHOCO:
                pass
            else :
                # DEBUG
                print("WARNING! tag that i doesn't know")
        # Check if the last element is a BackupPath or an Element of the tree (END)


        


        # Retrieve all the child elements of the popped_element and put in the stack
        for child in popped_element:
            stack_elements.append(child)

        # DEBUG
        print_element(popped_element)

        


    
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

    print()

    # Cleaning
    shutil.rmtree("garbage", ignore_errors=True)

    create_base_directories()

    # install_software("https://download.mozilla.org/?product=firefox-stub&os=win&lang=it", "firefox-installer.exe", "abla")

    testParseXml("resources.xml")