#!/usr/bin/env python
import subprocess
import os
import shutil

from pathlib import Path

import xml.etree.ElementTree as ET



from console_interface import CONSOLE_INTERFACE
from directories_handler import DIRECTORIES_HANDLER
from enviroment_variable_handler import ENV_VAR_HANDLER
from resources_handler import RESOURCES_HANDLER
from resources_handler import ResourceException





def parse_xml(name: str) -> None:

    class BackupPath:
        def __init__(self, path: str):
            self.intern = path

        def __str__(self):
            return "BackupPath: " + str(self.intern)
        
    class TAGS:
        DIRECTORY = "directory"
        RES = "resource"
        CHOCO = "chocolatey-dependencies"
        GROUP = "group"
        DATA = "data"
    
    class ATTRIB:
        NAME = "name"
        URL = "url"
        EXT = "extension"
        TYPE = "type"
        ENV = "add_to_enviroment_path_variable"
        MAN = "manually"
        INST = "install"
        INT_DIRS = "internal_dirs"

        # This function take the value of an attribute like a string and convert to a boolean
        # if it is possible.
        # Correct boolean value or false in case the value passed is None
        @staticmethod
        def retrieve_bool(attrib_value: str) -> None | bool:
            if attrib_value == None or len(attrib_value) != 4:
                return False

            attrib_value = attrib_value[0].upper() + attrib_value[1:].lower()
            if attrib_value == 'True':
                return True
            elif attrib_value == 'False':
                return False
            
            return False
        
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

    @staticmethod
    def print_element(e):
        if isinstance(e, BackupPath): 
            # print(str(e))
            CONSOLE_INTERFACE.print_line(str(e))
            
        elif type(e) is ET.Element:
            # print("Element: " + e.tag + " name: " + str(e.attrib) + " childs number: " + str(len(list(e))))
            CONSOLE_INTERFACE.print_line("Element: " + e.tag + " name: " + str(e.attrib) + " childs number: " + str(len(list(e))))



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
        # print("\n StackElements:")
        CONSOLE_INTERFACE.print_line("\n StackElements:")
        for element in stack_elements:
            print_element(element)
        # print("StackElements end")
        CONSOLE_INTERFACE.print_line("StackElements end")
        
        # Pop the last element
        popped_element = stack_elements.pop(len(stack_elements) - 1)

        # DEBUG
        # print("Popped element:")
        CONSOLE_INTERFACE.print_line("Popped element:")
        print_element(popped_element)

        # Check if the last element is a BackupPath or an Element of the tree (START)
        if isinstance(popped_element, BackupPath):
            # DEBUG
            # print(popped_element)
            CONSOLE_INTERFACE.print_line(str(popped_element))

            # Change effectevly the current working directory only if 
            # the current working directory is different from the directory 
            # where we must be
            # TODO verify that works properly
            if cwd_path != popped_element.intern:
                cwd_path = popped_element.intern
                os.chdir(cwd_path)
            continue

        elif type(popped_element) is ET.Element:
            if popped_element.tag == TAGS.DIRECTORY:
                # If the directory "cwd_path\popped_element.attrib['name']" 
                # doesn't exist create it
                popped_element_dir_path = os.path.join(cwd_path, popped_element.attrib[ATTRIB.NAME])
                if not os.path.isdir(popped_element_dir_path):
                    os.mkdir(popped_element_dir_path)

                # if the directory isn't empty and we are in another directory, 
                # change directory then save the current value of cwd_path in 
                # a BackupPath 
                if len(list(popped_element)) > 0:
                    stack_elements.append(BackupPath(cwd_path))
                    cwd_path = popped_element_dir_path
                    os.chdir(cwd_path)
            
            elif popped_element.tag == TAGS.RES:
                # Retrieve attributes' value from the element (START)
                url = popped_element.attrib.get(ATTRIB.URL)
                name = popped_element.attrib.get(ATTRIB.NAME)
                dir = cwd_path
                env_var = ATTRIB.retrieve_bool(popped_element.attrib.get(ATTRIB.ENV))
                
                install = ATTRIB.retrieve_bool(popped_element.attrib.get(ATTRIB.INST))
                manually_install = ATTRIB.retrieve_bool(popped_element.attrib.get(ATTRIB.MAN))
                extension = popped_element.attrib.get(ATTRIB.EXT)
                internal_dirs = popped_element.attrib.get(ATTRIB.INT_DIRS)

                if extension == None:
                    extension = ""

                if internal_dirs == None:
                    internal_dirs = []
                else:
                    internal_dirs = internal_dirs.split(",")
                    if len(internal_dirs) > 0 and internal_dirs[len(internal_dirs)-1] == "":
                        internal_dirs.pop()
                # Retrieve attributes' value from the element (END)

                # # Skip the resource if it is not valid
                # if RESOURCES_HANDLER.is_valid_resource(url, name, dir, env_var, install, manually_install, extension, internal_dirs):
                #     RESOURCES_HANDLER.provide_resource(url, name, dir, env_var, install, manually_install, extension, internal_dirs)
                # else:
                #     # DEBUG
                #     # TODO show error caused by the resource 
                #     pass
                try:
                    RESOURCES_HANDLER.provide_resource(url, name, dir, env_var, install, manually_install, extension, internal_dirs)
                except ResourceException as res_ex:
                    print(res_ex.message)

            elif popped_element.tag == TAGS.CHOCO:
                pass
            elif popped_element.tag == TAGS.GROUP:
                pass
            elif popped_element.tag == TAGS.DATA:
                pass
            else :
                # DEBUG
                CONSOLE_INTERFACE.print_line("WARNING! tag that i doesn't know")
        # Check if the last element is a BackupPath or an Element of the tree (END)

        # Retrieve all the child elements of the popped_element and put in the stack
        for child in popped_element:
            stack_elements.append(child)

        CONSOLE_INTERFACE.clear()


    
if __name__ == "__main__":

    DEBUG = True

    start_path = "C:/source/Python/windows-configurator"

    DIRECTORIES_HANDLER.init(start_path, DEBUG)
    RESOURCES_HANDLER.init(DEBUG)
    ENV_VAR_HANDLER.init(DEBUG)



    # TEMP
    os.chdir(start_path)

    # Cleaning
    shutil.rmtree("garbage", ignore_errors=True)

    CONSOLE_INTERFACE.init(DEBUG)
    CONSOLE_INTERFACE.print_logo()
    CONSOLE_INTERFACE.print_line("")

    DIRECTORIES_HANDLER.create_base_directories()

    parse_xml("resources.xml")

    CONSOLE_INTERFACE.print_line_at("Hello World!", [5 , 1])

    # TODO After all clean all the garbage(NOT IN DEBUG MODE) 

    CONSOLE_INTERFACE.close()
