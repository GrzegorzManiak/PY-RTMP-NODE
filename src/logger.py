from enum import Enum
import time

# -- Colors
WHITE = '\033[97m'
GREY = '\033[90m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
PURPLE = '\033[95m'



"""
    :name: LogLevel
    :desc: An "enum" for the different log levels
"""
class LogLevel(Enum):
    DEBUG = {
        'name': 'DEBUG',
        'color': BLUE
    }
    INFO = {
        'name':  'INFO',
        'color': GREEN
    }
    WARNING = {
        'name': 'WARNING',
        'color': YELLOW
    }
    ERROR = {
        'name': 'ERROR',
        'color': RED
    }
    CRITICAL = {
        'name': 'CRITICAL',
        'color': PURPLE
    }

    def __str__(self) -> str:
        return self.name

    def color(self) -> str:
        return self.value['color']

    def figure(value):
        if isinstance(value, LogLevel):
            return value

        for level in LogLevel:
            if level.name == value.upper():
                return level

        return LogLevel.INFO
    


"""
    :name: Logger
    :desc: A simple Logging function
"""
def log(
    header: str,
    message: str,
    level: LogLevel = LogLevel.INFO
) -> None:
    header = header.upper()
    level = LogLevel.figure(level)
    
    f_time = f'{GREY}[{int(time.time() * 1000)}]{WHITE}'
    tag = f'{level.color()}{str(level).ljust(8)} {str(header).ljust(8)}{WHITE}'
    print(f'{f_time} {tag} {message}')

    # -- IF Its a critical error, exit the script
    if level == LogLevel.CRITICAL:
        exit(1)