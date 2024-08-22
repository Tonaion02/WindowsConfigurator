import os





#===================================================================================================================
#-------------------------------------------------------------------------------------------------------------------
# CONSOLE_INTERFACE Class
# This is a full static Class
# This class contains methods(static) to print on the command line output for UI/debug purpose
# ANSI escape for move cursor:https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
# WARNING: don't use directly print, it can be break CONSOLE_INTERFACE
#-------------------------------------------------------------------------------------------------------------------
class CONSOLE_INTERFACE:

    END_OF_LOGO = [0, 0]
    __DEBUG = None
    __DEBUG_LOG_FILE = None





    # Init CONSOLE_INTERFACE
    def init(debug: bool) -> None:
        CONSOLE_INTERFACE.__DEBUG = debug
        if CONSOLE_INTERFACE.__DEBUG:
            CONSOLE_INTERFACE.__DEBUG_LOG_FILE = open("debug_log.txt", "w")

    # Back home with cursor (0, 0)
    # (encoding a tuple of numbers in ANSI)
    @staticmethod
    def __home_cursor_ansi() -> str:
        return '\x1b[H'
    
    # Set cursor position(encoding a string in ANSI)
    @staticmethod
    def __setc_ansi(t: list) -> str:
        return '\x1b[{};{}f'.format(t[0], t[1])

    # Set cursor position
    @staticmethod
    def __set_curs(t: list) -> None:
        print(CONSOLE_INTERFACE.__setc_ansi(t))

    # Back home cursor
    @staticmethod
    def __home_curs() -> None:
        print(CONSOLE_INTERFACE.__setc_ansi())

    # Print line in the CONSOLE_INTERFACE
    @staticmethod
    def print_line(line: str) -> None:
        print(line)
        if CONSOLE_INTERFACE.__DEBUG:
            CONSOLE_INTERFACE.__DEBUG_LOG_FILE.write(line + "\n")

    @staticmethod
    def print_line_at(line: str, pos: list) -> None:
        CONSOLE_INTERFACE.__set_curs(pos)
        print(line)
        if CONSOLE_INTERFACE.__DEBUG:
            CONSOLE_INTERFACE.__DEBUG_LOG_FILE.write(line + "\n")

    @staticmethod
    def print_logo() -> None:
        print(CONSOLE_COLORS.CYAN + "+===================================================================================================================+")
        print("|                                          WINDOWS-CONFIGURATOR                                                     |")
        print("+===================================================================================================================+" + CONSOLE_COLORS.WHITE)
        CONSOLE_INTERFACE.END_OF_LOGO = [3, 1]
        CONSOLE_INTERFACE.CURRENT_CURSOR_POS = CONSOLE_INTERFACE.END_OF_LOGO 

    @staticmethod
    def clear() -> None:
        os.system('cls')
        CONSOLE_INTERFACE.print_logo()

    @staticmethod
    def close() -> None:
        CONSOLE_INTERFACE.__DEBUG_LOG_FILE.close()

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