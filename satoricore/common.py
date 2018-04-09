from enum import Enum


class _STANDARD_EXT(Enum):
    DIRECTORY_T = 'D'
    FILE_T = 'F'
    LINK_T = 'L'
    BLOCK_DEVICE_T = 'B'
    CHAR_DEVICE_T = 'C'
    FIFO_T = 'I'
    SOCKET_T = 'S'
    UNKNOWN_T = 'U'
