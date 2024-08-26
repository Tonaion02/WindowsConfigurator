import requests
import os
import zipfile
from pathlib import Path

import magic

from directories_handler import DIRECTORIES_HANDLER 
from enviroment_variable_handler import ENV_VAR_HANDLER





#===================================================================================================================
#-------------------------------------------------------------------------------------------------------------------
# RESOURCES_HANDLER Class
# This is a full static Class
# This class contains methods(static) to handle resources
#-------------------------------------------------------------------------------------------------------------------
class RESOURCES_HANDLER:

    __DEBUG = False



    # Init RESOURCES_HANDLER
    @staticmethod
    def init(debug: bool) -> None:
        RESOURCES_HANDLER.__DEBUG = debug



    # Unique function to provide a resourse from his attributes
    # describing parameters:
    # url:              url from we can download the resource
    # name:             name that we give to resource
    # dir:              directory where we want to place resource
    # env_var:          bool that indicates if we want to add or not the path(dir/name) to resource to PATH enviroment variable
    # install:          bool that indicates if we want to install or not the resource
    # manually_install: bool that indicates if the resource must be installed manually, we put the resource under INTERNAL_DIRECTORIES.TO_MANUALLY_INSTALL_DIR
    # extension:        str that indicates the extension of the resource
    # internal_dirs:    this list of str indicates internal directories that we want to add to PATH enviroment variable, so for each element 'internal_dir' of the directories we put in PATH dir/name/internal_dir
    @staticmethod
    # TODO add a variable for the arguments of the installers
    # TODO 
    def provide_resource(url: str, name: str, dir: str, env_var: bool, install: bool, manually_install: bool, extension: str, internal_dirs: list[str]):
        # Retrieve the resource from the url
        response = requests.get(url, allow_redirects=True)
        if response.status_code != 200:
            raise ConnectionError('could not download {}\nerror code: {}'.format(url, response.status_code))
        


        path_to_file = None

        # Search for extension if it is not already setted from
        # the userim
        if extension == "":
            extension = RESOURCES_HANDLER.__retrieve_file_extension(url, response)

        # Check if the resource downloaded is valid
        # in other case launch exception
        if RESOURCES_HANDLER.__is_valid_resource(url, name, dir, env_var, install, manually_install, extension, internal_dirs) == False:
            raise ResourceException("The attribute of this resource is not valid")

        # Archive case (START)        
        # For now consider only the .zip file extension
        # TODO
        # For now consider only the portable application
        # (ignore that the output can be anything different 
        # than a folder)
        # TODO
        if extension != "":
            if extension == "zip":
                path_to_file = os.path.join(dir, name)

                temp_path_to_archive = os.path.join(DIRECTORIES_HANDLER.DOWNLOADS_DIR, name + "." + extension)
                temp_path_to_archive = Path(temp_path_to_archive)
                temp_path_to_archive.write_bytes(response.content)

                with zipfile.ZipFile(temp_path_to_archive, 'r') as zip_ref:
                    zip_ref.extractall(path_to_file)
        # Archive case (END)



        if extension != "":
            # apply the extension to the name of the file
            name = name + "." + extension

        if install == True:
            # TODO install, but before put in downloadsTmp
            pass

        if manually_install == True:
            # compute a path to the directory to manually install softwares
            path_to_file = os.path.join(DIRECTORIES_HANDLER.TO_MANUALLY_INSTALL_DIR, name)
            PATH_path_to_file = Path(path_to_file)
            PATH_path_to_file.write_bytes(response.content)

        # if the resource is not an installer or an archive
        # save directly the resource to filesystem
        if install == False and manually_install == False:
            # TODO consider other archives
            if extension not in ['zip']:
                path_to_file = os.path.join(dir, name)
                PATH_path_to_file = Path(path_to_file)
                PATH_path_to_file.write_bytes(response.content)

        if env_var == True:
            # Update the PATH enviroment variable with the new path 
            # to this portable file if it is needed
            ENV_VAR_HANDLER.update_enviroment_variable("PATH", path_to_file + ";")

        if internal_dirs != "":
            # Update the PATH enviroment variable with internal dirs
            # to this portable file
            for internal_dir in internal_dirs:
                internal_dir = os.path.join(path_to_file, internal_dir)
                ENV_VAR_HANDLER.update_enviroment_variable("PATH", internal_dir + ";")

    @staticmethod
    def __is_valid_resource(url: str, name: str, dir: str, env_var: bool, install: bool, manually_install: bool, extension: str, internal_dirs: list[str]):

        # ERROR if (no)extension + install(we can't install without being sure about the extension)
        if extension == "" and install == True:
            return False

        # ERROR if manually_install + install
        if install == True and manually_install == True:
            return False

        return True

    # This methods retrieve extension of the file that is 
    # the resource that we are trying to download.
    # TODO optimize we can simply save before the file
    # and next move the file in the correct
    # location 
    @staticmethod
    def __retrieve_file_extension(url : str, response) -> str:

        # Try first with Content-Disposition of the response
        file_name = RESOURCES_HANDLER.__retrieve_file_name_from_response(response)

        if file_name != None:
            found = file_name.rfind(".")
            if found != -1:
                return file_name[found+1:]

        # # Try with the url
        # last_slash_index = url.rfind("/")
        # if last_slash_index != -1 and last_slash_index+1 < len(url):
        #     return url[last_slash_index:]

        # TODO
        # Try with Content-Type of the response

        # Determinize extension with magic
        # TODO optimize here
        temp_file = "temporary_to_determine_extension"
        path_to_temp_file = os.path.join(DIRECTORIES_HANDLER.DOWNLOADS_DIR, temp_file)
        PATH_to_temp_file = Path(path_to_temp_file)
        PATH_to_temp_file.write_bytes(response.content)
        extension = magic.from_file(path_to_temp_file, mime=True)
        extension = extension[extension.find("/")+1:]
        # particular cases
        if extension.find("exe") != -1:
            extension = "exe"

        return extension

    # This methods try to retrieve the file's name from 
    # the header 'Content-Disposition' of the 
    # HTTPS response
    @staticmethod
    def __retrieve_file_name_from_response(response) -> str | None:
        # Content-Disposition is an header of a response
        # The Content-Disposition contains the name of the downloaded file
        # We use the name of the downloaed file to check if it is a zip or a Rar etc
        content_disposition = response.headers.get('Content-Disposition')

        if content_disposition == None:
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
#===================================================================================================================



#===================================================================================================================
#-------------------------------------------------------------------------------------------------------------------
# ResourceException class
# Custom exception for the resources
#-------------------------------------------------------------------------------------------------------------------
class ResourceException(RuntimeError):
    def __init__(self, message):
        self.message = message
#===================================================================================================================