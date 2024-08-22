import os





#===================================================================================================================
# ------------------------------------------------------------------------------------------------------------------
# Class ENV_VAR_HANDLER
# It is a full static class
# This class contains methods(static) to set or update the value of enviroment variable
# TODO setup the class in a way that we can define a debug mode
# ------------------------------------------------------------------------------------------------------------------
class ENV_VAR_HANDLER:

    # Modify or create an enviroment variable PERMANENTLY
    # PERMANENTLY means that the changes are not local to this shell
    # Note: It already adds " to value to support spaces in value
    # TODO try to create a Class to cache the real save to a variable
    @staticmethod
    def setX(name: str, value: str) -> None:
        os.system("SETX " + name + " \"" + value + "\"")

    # Update the current value of an enviroment variable
    @staticmethod
    def update_enviroment_variable(name: str, value: str) -> None:
        # DEBUG
        # TODO 
        name = "TEMP_PATH"

        prev_value = os.environ.get(name)
        if prev_value == None:
            prev_value = ""

        os.system("SETX " + name + " " + prev_value + "\"" + value + "\"")
        os.environ[name] = prev_value + value
#===================================================================================================================