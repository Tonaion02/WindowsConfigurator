import os





#===================================================================================================================
# ------------------------------------------------------------------------------------------------------------------
# Class ENV_VAR_HANDLER
# It is a full static class
# This class contains methods(static) to set or update the value of enviroment variable
# ------------------------------------------------------------------------------------------------------------------
class ENV_VAR_HANDLER:

    __DEBUG = False

    # Init the ENV_VAR_HANDLER
    @staticmethod
    def init(debug: bool) -> None:
        ENV_VAR_HANDLER.__DEBUG = debug

    # Modify or create an enviroment variable PERMANENTLY
    # PERMANENTLY means that the changes are not local to this shell
    # NOTE: It already adds " to value to support spaces in value
    # TODO try to create a Class to cache the real save to a variable
    # TODO verify if it is useless
    @staticmethod
    def setX(name: str, value: str) -> None:
        os.system("SETX " + name + " \"" + value + "\"")

    # Update the current value of an enviroment variable PERMANENTLY
    # PERMANENTLY means that the changes are not local to this shell
    # NOTE: It already adds " to value to support spaces in value
    # NOTE: in that os.environ is used only to mantain in memory
    # during the execution the updated value of the enviroment variable
    # the real save is made with the command SETX
    @staticmethod
    def update_enviroment_variable(name: str, value: str) -> None:
        if ENV_VAR_HANDLER.__DEBUG == True:
            name = "TEMP_PATH"

        prev_value = os.environ.get(name)
        if prev_value == None:
            prev_value = ""

        os.system("SETX " + name + " " + prev_value + "\"" + value + "\"")
        os.environ[name] = prev_value + value
#===================================================================================================================