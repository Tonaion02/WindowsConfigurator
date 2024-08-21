#!/usr/bin/env python
import subprocess
import os
import shutil

from pathlib import Path
import requests

import xml.etree.ElementTree as ET

import zipfile

from console_interface import CONSOLE_INTERFACE

from directories_handler import DIRECTORIES_HANDLER





DIRECTORIES_HANDLER.init("C:/source/Python/windows-configurator")





def install_software_test(url: str, outfile, installation_directory=None):
    R = requests.get(url, allow_redirects=True)
    if R.status_code != 200:
        raise ConnectionError('could not download {}\nerror code: {}'.format(url, R.status_code))
    
    outfile = os.path.join(DIRECTORIES_HANDLER.DOWNLOADS_DIR, outfile)
    pathOutFile = Path(outfile)
    pathOutFile.write_bytes(R.content)

    if installation_directory == None:
        print("Da fare!!!")
    else:
        # subprocess.Popen(outfile + "/S /InstallDirectoryPath=\"C:/test/firefox\"", shell=True)
        res = os.system("choco.exe ")
        print(res)

# This methods retrive file_name from an the headers of an HTTP response
def retrieve_file_name_from_response(response) -> str | None:
    # Content-Disposition is an header of a response
    # The Content-Disposition contains the name of the downloaded file
    # We use the name of the downloaed file to check if it is a zip or a Rar etc
    content_disposition = response.headers.get('Content-Disposition')
        
    # DEBUG
    # TODO add exception
    if content_disposition == None:
        print("There isn't Content-Disposition in response's headers")
        return None

    contents = content_disposition.split()

    # Retrieve filename from the Content-Disposition
    file_name = None
    for content in contents:
        found = content.find('filename')

        if found >= 0:
            index = content.find("=")
            file_name = content[index + 1:]
            break

    return file_name

# Simply routine to download a file at url=url, renamed with name=name and 
# saved in a the directory=dir
# TODO check if the file already exist, in the case launch exception
def download_file(url: str, name: str, dir: str) -> None:
    response = requests.get(url, allow_redirects=True)
    if response.status_code != 200:
        raise ConnectionError('could not download {}\nerror code: {}'.format(url, response.status_code))

    name_downloaded_file = retrieve_file_name_from_response(response)
    if name_downloaded_file != None:
        name_downloaded_file = name_downloaded_file.replace("\"", "")
        name = name_downloaded_file

    path_to_file = os.path.join(dir, name)
    path_to_file_PATH = Path(path_to_file)
    path_to_file_PATH.write_bytes(response.content)

# Routine to download and install(if it is needed) a software
# In the case of a portable file, it automatically understand if it 
# is needed to unzip/unrar the file. We can specify if it is portable
# with portable paramter.
# With update_env_path_var parameter we specify if we must add the path
# to the file or .exe to the enviroment variable
def install_software(url: str, name: str, dir: str, portable: bool, update_env_path_var: bool):

    response = requests.get(url, allow_redirects=True)
    if response.status_code != 200:
        raise ConnectionError('could not download {}\nerror code: {}'.format(url, response.status_code))

    path_to_file = os.path.join(dir, name)

    if portable:    
        # # Content-Disposition is an header of a response
        # # The Content-Disposition contains the name of the downloaded file
        # # We use the name of the downloaed file to check if it is a zip or a Rar etc
        # content_disposition = response.headers.get('Content-Disposition')
        
        # # DEBUG
        # if content_disposition == None:
        #     print("There isn't Content-Disposition in response's headers")
        # contents = content_disposition.split()

        # # Retrieve filename from the Content-Disposition
        # file_name = None
        # for content in contents:
        #     found = content.find('filename')

        #     if found >= 0:
        #         index = content.find("=")
        #         file_name = content[index + 1:]
        #         break

        file_name = retrieve_file_name_from_response(response)

        # DEBUG
        # TODO improve this error and launch an Exception
        if file_name == None:
            print("Error file_name is None")

        temp_path_to_archive = os.path.join(DIRECTORIES_HANDLER.DOWNLOADS_DIR, file_name)
        temp_path_to_archive = Path(temp_path_to_archive)
        temp_path_to_archive.write_bytes(response.content)

        # For now consider only the .zip file extension
        # TODO
        found = file_name.find(".zip")
        if found != -1:
            with zipfile.ZipFile(temp_path_to_archive, 'r') as zip_ref:
                zip_ref.extractall(path_to_file)
        else:
            print("Error not .zip")

        # Update the PATH enviroment variable with the new path to this portable file
        # if it is needed
        if update_env_path_var:
            update_enviroment_variable("PATH", path_to_file + ";") 
        

    elif not portable:
        # TODO
        pass





# Modify or create an enviroment variable PERMANENTLY
# PERMANENTLY means that the changes are not local to this shell
# Note: It already adds " to value to support spaces in value
# TODO try to create a Class to cache the real save to a variable
def setX(name: str, value: str) -> None:
    os.system("SETX " + name + " \"" + value + "\"")

# Update the current value of an enviroment variable
def update_enviroment_variable(name: str, value: str) -> None:
    # DEBUG
    # TODO 
    name = "TEMP_PATH"
    
    prev_value = os.getenv(name)
    if prev_value == None:
        prev_value = ""

    prev_value_ = os.environ.get(name)
    if prev_value_ == None:
        prev_value_ = ""

    os.system("SETX " + name + " \"" + prev_value + value + "\"")
    os.environ[name] = " \"" + prev_value_ + value + "\""




# TEMP
def parse_xml(name: str) -> None:

    class BackupPath:
        def __init__(self, path: str):
            self.intern = path

        def __str__(self):
            return "BackupPath: " + str(self.intern)
        
    class TAGS:
        DIRECTORY = "directory"
        FILE = "file"
        SOFTWARE = "software"
        CHOCO = "chocolatey-dependencies"
        GROUP = "group"
        DATA = "data"
    
    class ATTRIB:
        NAME = "name"
        URL = "url"
        EXT = "extension"
        TYPE = "type"
        ENV = "add_to_enviroment_path_variable"

        # This function take a the value of an attribute like a string and convert to a boolean
        # if it is possible.
        # Correct boolean value or a number(3) in case of error
        # WARNING: for the use of '|' operator that create some sort of Union, we must use
        # and support only Python 3.10
        @staticmethod
        def retrieve_bool(attrib_value: str) -> int | bool:
            if attrib_value == None or len(attrib_value) != 4:
                return 3

            attrib_value = attrib_value[0].upper() + attrib_value[1:].lower()
            if attrib_value == 'True':
                return True
            elif attrib_value == 'False':
                return False

            return 3
        
        # Methods(static) to verify that value of attribute named 'type' is valid or has a specific value (START)
        @staticmethod
        def is_valid_software_type(type_: str) -> bool:
            return type_ in ['portable', 'installable', 'manually']
        
        @staticmethod
        def is_portable(type_: str) -> bool:
            return type_ == 'portable'
        
        @staticmethod
        def is_installable(type_: str) -> bool:
            return type_ == 'installable'
        
        @staticmethod
        def is_manually_installable(type_: str) -> bool:
            return type_ == 'manually'
        # Methods(static) to verify that value of attribute named 'type' is valid or has a specific value (END)

    def print_element(e):
        if isinstance(e, BackupPath): 
            print(str(e))
            
        elif type(e) is ET.Element:
            print("Element: " + e.tag + " name: " + str(e.attrib) + " childs number: " + str(len(list(e))))



    # Variable that mantain the path of the current working directory like a string
    cwd_path = DIRECTORIES_HANDLER.BASE_DIR  

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

        # DEBUG
        print("Popped element:")
        print_element(popped_element)

        # Check if the last element is a BackupPath or an Element of the tree (START)
        if isinstance(popped_element, BackupPath):
            # DEBUG
            print(popped_element)

            # Change effectevly the current working directory only if the current working directory
            # is different from the directory where we must be
            # TODO verify that works properly
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
                # Download file, rename it(with correct extension) and put it in the right folder (START)
                url = popped_element.attrib[ATTRIB.URL]
                name = popped_element.attrib[ATTRIB.NAME]
                extension = popped_element.attrib[ATTRIB.EXT]
                dir = cwd_path
                name = name + "." + extension
                download_file(url, name, dir)
                # Download file, rename it(with correct extension) and put it in the right folder (END)

            elif popped_element.tag == TAGS.SOFTWARE:
                url = popped_element.attrib.get(ATTRIB.URL)
                name = popped_element.attrib.get(ATTRIB.NAME)
                dir = cwd_path
                type_ = popped_element.attrib.get(ATTRIB.TYPE)
                env_var = ATTRIB.retrieve_bool(popped_element.attrib.get(ATTRIB.ENV))



                # DEBUG
                # TODO improve (No exception is needed, we handle it here)
                if not ATTRIB.is_valid_software_type(type_):
                    print("Value: " + str(type_) + " is not a valid value for the type of software")

                if ATTRIB.is_portable(type_):
                    install_software(url, name, dir, True, env_var)

                if ATTRIB.is_manually_installable(type_):
                    download_file(url, name, DIRECTORIES_HANDLER.TO_MANUALLY_INSTALL_DIR)

                if ATTRIB.is_installable(type_):
                    # TODO
                    pass
            
            elif popped_element.tag == TAGS.CHOCO:
                pass
            elif popped_element.tag == TAGS.GROUP:
                pass
            elif popped_element.tag == TAGS.DATA:
                pass
            else :
                # DEBUG
                print("WARNING! tag that i doesn't know")
        # Check if the last element is a BackupPath or an Element of the tree (END)

        # Retrieve all the child elements of the popped_element and put in the stack
        for child in popped_element:
            stack_elements.append(child)

      


    
if __name__ == "__main__":

    CONSOLE_INTERFACE.print_logo()

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

    DIRECTORIES_HANDLER.create_base_directories()

    # install_software("https://download.mozilla.org/?product=firefox-stub&os=win&lang=it", "firefox-installer.exe", "abla")

    parse_xml("resources.xml")

    # After all clean all the garbage(NOT IN DEBUG MODE) TODO

    # TEMP
    update_enviroment_variable("PATH", "hello" + ";")