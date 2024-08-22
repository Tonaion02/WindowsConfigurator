import os





#===================================================================================================================
#-------------------------------------------------------------------------------------------------------------------
# CONSOLE_INTERFACE Class
# This is a full static Class
# This class contains methods(static) to print on the command line output for UI/debug purpose
# ANSI escape for move cursor:https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
#-------------------------------------------------------------------------------------------------------------------
class CONSOLE_INTERFACE:

    END_OF_LOGO = (0, 0)



    # Back home with cursor (0, 0)
    @staticmethod
    def __home_cursor_ansi() -> str:
        return '\x1b[H'
    
    # Set cursor position
    @staticmethod
    def __setc_ansi(t: tuple) -> str:
        return '\x1b[{};{}f'.format(t[0], t[1])

    @staticmethod
    def print_logo() -> None:
        os.system('cls')

        print(CONSOLE_COLORS.CYAN + "+===================================================================================================================+")
        print("|                                          WINDOWS-CONFIGURATOR                                                     |")
        print("+===================================================================================================================+" + CONSOLE_COLORS.WHITE)

        CONSOLE_INTERFACE.END_OF_LOGO = (3, 1) 
        print("===================================================================" + CONSOLE_INTERFACE.__setc_ansi((1, 1)) + "Hello")
        print(CONSOLE_INTERFACE.__setc_ansi((5, 1)))

#===================================================================================================================



#===================================================================================================================
#-------------------------------------------------------------------------------------------------------------------
# CONSOLE_COLORS Class
# Ansi escape for colors
# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
# https://ss64.com/nt/syntax-ansi.html#:~:text=Specify%20the%20color%20codes%20in,back%20to%20the%20default%20colors.
#-------------------------------------------------------------------------------------------------------------------
class CONSOLE_COLORS:
    WHITE = '\033[97m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
#===================================================================================================================