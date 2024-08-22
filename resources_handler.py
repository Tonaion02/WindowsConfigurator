import requests
import os
import zipfile
from pathlib import Path

from directories_handler import DIRECTORIES_HANDLER 
from enviroment_variable_handler import ENV_VAR_HANDLER





#===================================================================================================================
#-------------------------------------------------------------------------------------------------------------------
# RESOURCES_HANDLER Class
# This is a full static Class
# This class contains methods(static) to handle resources
#-------------------------------------------------------------------------------------------------------------------
class RESOURCES_HANDLER:

    @staticmethod
    # TODO add a variable for the arguments of the installers
    # TODO 
    def provide_resource(url: str, name: str, dir: str, env_var: bool, install: bool, manually_install: bool, extension: str):
        # Retrieve the resource from the url
        response = requests.get(url, allow_redirects=True)
        if response.status_code != 200:
            raise ConnectionError('could not download {}\nerror code: {}'.format(url, response.status_code))
        


        path_to_file = None

        # Archive case (START)
        # TODO check if we have always file_name for the .zip/.rar
        file_name = RESOURCES_HANDLER.retrieve_file_name_from_response(response)

        # DEBUG
        # TODO only an info now?
        if file_name == None:
            print("file_name is None")

        # For now consider only the .zip file extension
        # TODO
        # For now consider only the portable application
        # (ignore that the output can be anything different 
        # than a folder)
        # TODO
        # Check if have extension
        # TODO
        if file_name != None:
            found = file_name.find(".zip")
            if found != -1:
                path_to_file = os.path.join(dir, name)

                temp_path_to_archive = os.path.join(DIRECTORIES_HANDLER.DOWNLOADS_DIR, file_name)
                temp_path_to_archive = Path(temp_path_to_archive)
                temp_path_to_archive.write_bytes(response.content)

                with zipfile.ZipFile(temp_path_to_archive, 'r') as zip_ref:
                    zip_ref.extractall(path_to_file)
            else:
                print("not .zip")
        # Archive case (END)



        if extension == True:
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

        if env_var == True:
            # Update the PATH enviroment variable with the new path 
            # to this portable file if it is needed
            ENV_VAR_HANDLER.update_enviroment_variable("PATH", path_to_file + ";") 

    @staticmethod
    # TODO
    def is_valid_resource(url: str, name: str, dir: str, env_var: bool, install: bool, manually_install: bool, extension: str):

        # ERROR if (no)extension + install(we can't install without being sure about the extension)
        if extension == "" and install == True:
            return False

        # ERROR if manually_install + install
        if install == True and manually_install == True:
            return False

        return True

    # This methods retrive file_name from an the headers of an HTTP response
    @staticmethod
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




















    # TEMP
    @staticmethod
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



    # Simply routine to download a file at url=url, renamed with name=name and 
    # saved in a the directory=dir
    # TODO check if the file already exist, in the case launch exception
    @staticmethod
    def download_file(url: str, name: str, dir: str) -> None:
        response = requests.get(url, allow_redirects=True)
        if response.status_code != 200:
            raise ConnectionError('could not download {}\nerror code: {}'.format(url, response.status_code))

        # Trying to understand if we can understand the extension of the file automatically
        # TODO
        name_downloaded_file = RESOURCES_HANDLER.retrieve_file_name_from_response(response)
        if name_downloaded_file != None:
            name_downloaded_file = name_downloaded_file.replace("\"", "")
            name = name_downloaded_file

        path_to_file = os.path.join(dir, name)
        path_to_file_PATH = Path(path_to_file)
        path_to_file_PATH.write_bytes(response.content)

    # Routine to download and install(if it is needed) a software
    # In the case of a portable file, it try to automatically understand if it 
    # is needed to unzip/unrar the file. In some case is already necessary to
    # specify. We can specify if it is portable with portable parameter.
    # With update_env_path_var parameter we specify if we must add the path
    # to the file or .exe to the enviroment variable
    @staticmethod
    def install_software(url: str, name: str, dir: str, portable: bool, update_env_path_var: bool):

        response = requests.get(url, allow_redirects=True)
        if response.status_code != 200:
            raise ConnectionError('could not download {}\nerror code: {}'.format(url, response.status_code))

        path_to_file = os.path.join(dir, name)

        if portable:    
            file_name = RESOURCES_HANDLER.retrieve_file_name_from_response(response)

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
                ENV_VAR_HANDLER.update_enviroment_variable("PATH", path_to_file + ";") 


        elif not portable:
            # TODO
            pass
#===================================================================================================================