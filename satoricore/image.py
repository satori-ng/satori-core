import os
import os.path
import platform

import satoricore
from satoricore.common import _STANDARD_EXT

# Those tags will end up in the __data dict several times
# _S for Tag
# _T for Type
# Here they can be globally minified
_TYPE_S = 'type'
_CONTENTS_S = 'contents'
_SIZE_S = 'filesize'


class FileNotFoundError(Exception):
    pass


class NotADirectoryError(Exception):
    pass


class SatoriImage(object):

    # listdir = get_dir_contents
    def __init__(self):
        self.__data = {}
        self.__data['metadata'] = {}
        self.__data['metadata']['satori'] = {}
        self.__data['metadata']['system'] = {}
        self.__data['data'] = {}
        self.__data['data']['filesystem'] = {}
        # self.__data['data']['commands'] = {}

        self.__data['metadata']['satori']['version'] = satoricore.__version__
        self.__data['metadata']['satori']['extensions'] = []

        self.__data['metadata']['system']['type'] = platform.system()
        self.__data['metadata']['system']['user'] = os.getlogin()
        self.__data['metadata']['system']['platform'] = platform.platform()
        self.__data['metadata']['system']['hostname'] = platform.node()
        self.__data['metadata']['system']['machine'] = platform.machine()
        self.__data['metadata']['system']['release'] = platform.release()
        self.__data['metadata']['system']['processor'] = platform.processor()
        self.__data['metadata']['system']['specifics'] = {}
        # try :
        #     self.__data['metadata']['system']['specifics']['win'] = \
        #        platform.win32_ver()
        # except :
        #     pass
        # try :
        #     self.__data['metadata']['system']['specifics']['mac'] = \
        #        platform.mac_ver()
        # except :
        #     pass

    def _get_data_struct(self):
        return self.__data

    def _set_data_struct(self, data_struct):
        self.__data = data_struct

    def set_metadata(self, attr_dict, metadata_type, ):

        pass

    def add_file(self, full_path):
        self.set_attribute(full_path, {}, _CONTENTS_S, force_create=True)

    def set_attribute(self, full_path, attr_dict,
                      ext_name, force_create=False):
        """
        Adds an attribute to a file specified in the 'full_path'
        and creates it if it doesn't exist.
        """
        file_dict = self.__get_file_dict(full_path, force_create=force_create)
        # if ext_name not in _STANDARD_EXT:
        #     self.__data['metadata']['satori']['extensions'].append(ext_name)
        file_dict[ext_name] = attr_dict
        return file_dict

    def __get_file_dict(self, full_path, force_create=False):
        """
        Returns the 'dict' object for the 'full_path' specified.
        If 'force_create' is enabled and the 'full_path' does not exist,
        a dict is automatically created for that path
        """
        # Eliminate trailing '/' to make splitting easier
        if full_path.endswith(os.sep):
            full_path = full_path[:-1]
        # Get a list from the separated path
        path_tokens = full_path.split(os.sep)
        # path_tokens = [token for token in path_tokens if token]
        cur_position = self.__data['data']['filesystem']
        for token in path_tokens[:-1]:
            # Try accessing the file dict
            # cur_position = cur_position[token]
            if not force_create:
                continue

            try:
                # Try Accessing directory contents
                if _CONTENTS_S not in cur_position[token].keys():
                    raise NotADirectoryError(
                            "File: '{}' in Path: '{}' is not a Directory"
                            .format(token, full_path))
                # cur_position[token][_CONTENTS_S]
            except KeyError:
                # Directory doesn't exist - create it
                cur_position[token] = {
                    _CONTENTS_S: {},
                    _TYPE_S: _STANDARD_EXT.DIRECTORY_T,
                }

            cur_position = cur_position[token][_CONTENTS_S]

        # Create a file as an empty dict
        file_token = path_tokens[-1]
        if file_token not in cur_position.keys():
            cur_position[file_token] = {}
        return cur_position[file_token]

    def get_dir_contents(self, full_path):
        dir_dict = self.__get_file_dict(full_path)
        print(dir_dict.keys())
        if _CONTENTS_S not in dir_dict.keys():
            raise FileNotFoundError("Does not exist: '{}'".format(full_path))
        if dir_dict[_TYPE_S] != _STANDARD_EXT.DIRECTORY_T:
            raise NotADirectoryError("Not a directory: '{}'".format(full_path))
        return dir_dict[_CONTENTS_S].keys()


    def __str__(self):
        return self.__data.__str__()

    def __repr__(self):
        return self.__data.__repr__()

    def __eq__(self, rhs):
        # return self.__data == rhs._get_data_struct
        return repr(self) == repr(rhs)