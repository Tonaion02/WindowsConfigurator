import os





#===================================================================================================================
# ------------------------------------------------------------------------------------------------------------------
# DIRECTORIES_HANDLER class 
# DIRECTORIES_HANDLER is a full static class
# It builds and contains all the paths necessary for this program
# WARNING: to use this class properly is necessary to execute init before to use any of
# the methods of this class.
# TODO: necessary to move debug and the concept of the mode in a global part
# TODO: necessary to understand what to do where i am not in debug mode with the BASE_DIR
# what directory become the BASE_DIR?
# TODO: necessary rebase all the paths from a full path
# ------------------------------------------------------------------------------------------------------------------
class DIRECTORIES_HANDLER:

    # Change these names if you want to change directories' name (START)
    _GARBAGE_DIR = "garbage"
    _DOWNLOADS_DIR = "downloadsTmp"
    _TO_MANUALLY_INSTALL_DIR = "toManuallyInstall"
    _BASE_DIR = ""
    # Change these names if you want to change directories' name (END)

    GARBAGE_DIR = None
    DOWNLOADS_DIR = None
    BASE_DIR = None
    TO_MANUALLY_INSTALL_DIR = None

    # Don't touch this, PRIVATE (START)
    _debug = True



    @staticmethod
    def _get_garbage_dir():
        return DIRECTORIES_HANDLER._GARBAGE_DIR
    
    @staticmethod
    def _get_base_dir():
        return DIRECTORIES_HANDLER._BASE_DIR

    @staticmethod
    def _get_downloads_dir():
        return os.path.join(DIRECTORIES_HANDLER._BASE_DIR, DIRECTORIES_HANDLER._DOWNLOADS_DIR)
    
    @staticmethod
    def _get_to_manually_install_dir():
        return os.path.join(DIRECTORIES_HANDLER._BASE_DIR, DIRECTORIES_HANDLER._TO_MANUALLY_INSTALL_DIR)
    # Don't touch this, PRIVATE (END)



    @staticmethod
    def init(path: str):
        if DIRECTORIES_HANDLER._debug:
            DIRECTORIES_HANDLER._BASE_DIR = os.path.join(path, DIRECTORIES_HANDLER._GARBAGE_DIR)

            DIRECTORIES_HANDLER.GARBAGE_DIR = DIRECTORIES_HANDLER._get_garbage_dir()
            DIRECTORIES_HANDLER.DOWNLOADS_DIR = DIRECTORIES_HANDLER._get_downloads_dir()
            DIRECTORIES_HANDLER.BASE_DIR = DIRECTORIES_HANDLER._get_base_dir()
            DIRECTORIES_HANDLER.TO_MANUALLY_INSTALL_DIR = DIRECTORIES_HANDLER._get_to_manually_install_dir()
        else:
            pass # SYSTEM_BASE_DIR



    @staticmethod
    def create_base_directories():
        # Create garbage directory for garbage with name DIRECTORIES_HANDLER.GARBAGE_DIR
        os.mkdir(DIRECTORIES_HANDLER.GARBAGE_DIR)

        # Create downloads directory for downloads with name DIRECTORIES_HANDLER.DOWNLOADS_DIR
        os.mkdir(DIRECTORIES_HANDLER.DOWNLOADS_DIR)

        # Create manually install directories
        os.mkdir(DIRECTORIES_HANDLER.TO_MANUALLY_INSTALL_DIR)

#===================================================================================================================
