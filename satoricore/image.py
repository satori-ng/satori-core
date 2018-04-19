import os
import os.path
import threading
import pathlib

from satoricore.common import _STANDARD_EXT

# Those tags will end up in the __data dict several times
# _S for Tag
# _T for Type
# Here they can be globally minified
_TYPE_S = 'type'
_CONTENTS_S = 'contents'
_SIZE_S = 'size'

posixsep = pathlib.posixpath.sep
ntsep = pathlib.ntpath.sep


class SatoriImage(object):

    # listdir = get_dir_contents
    def __init__(self):
        self.__data = {}
        self.__data['metadata'] = {}
        self.__data['data'] = {}
        self.__data['data']['filesystem'] = {}

    def _get_data_struct(self):
        return self.__data

    def _set_data_struct(self, data_struct):
        self.__data = data_struct

    def set_metadata(self, attr_dict, metadata_type):
        self.__data['metadata'][metadata_type] = attr_dict

    def add_file(self, full_path):
        with threading.Lock():
            self.set_attribute(full_path, {}, _CONTENTS_S, force_create=True)
            self.set_attribute(
                full_path,
                _STANDARD_EXT.UNKNOWN_T,
                _TYPE_S,
                force_create=False,
            )

    def get_attribute(self, full_path, attr):
        return self.__get_file_dict(full_path).get(attr, {})

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

    def __get_file_dict(self, full_path, force_create=False, sep=os.path.sep):
        """
        Returns the 'dict' object for the 'full_path' specified.
        If 'force_create' is enabled and the 'full_path' does not exist,
        a dict is automatically created for that path
        """
        # Eliminate trailing '/' to make splitting easier
        if full_path.endswith(sep):
            full_path = full_path[:-1]
        # Get a list from the separated path
        path_tokens = full_path.split(sep)
        # path_tokens = [token for token in path_tokens if token]
        cur_position = self.__data['data']['filesystem']
        for token in path_tokens[:-1]:
            try:
                # Try Accessing directory contents
                if _CONTENTS_S not in cur_position[token].keys():
                    raise NotADirectoryError(
                            "File: '{}' in Path: '{}' is not a Directory"
                            .format(token, full_path))
                # cur_position[token][_CONTENTS_S]
            except KeyError:
                # Directory doesn't exist - create it
                if force_create:
                    cur_position[token] = {
                        _CONTENTS_S: {},
                        _TYPE_S: _STANDARD_EXT.DIRECTORY_T,
                    }
                else:
                    raise FileNotFoundError(
                        "Does not exist: '{}'".format(full_path)
                    )

            cur_position = cur_position[token][_CONTENTS_S]

        # Create a file as an empty dict
        file_token = path_tokens[-1]
        if file_token not in cur_position.keys() and force_create:
            cur_position[file_token] = {}

        try:
            return cur_position[file_token]
        except KeyError:
            raise FileNotFoundError("Does not exist: '{}'".format(full_path))

    def get_dir_contents(self, full_path):
        dir_dict = self.__get_file_dict(full_path)

        if _CONTENTS_S not in dir_dict.keys():
            raise FileNotFoundError("Does not exist: '{}'".format(full_path))
        if dir_dict[_TYPE_S] != _STANDARD_EXT.DIRECTORY_T:
            raise NotADirectoryError("Not a directory: '{}'".format(full_path))
        return dir_dict[_CONTENTS_S].keys()

    def listdir(self, full_path):
        return self.get_dir_contents(full_path)

    def __str__(self):
        return self.__data.__str__()

    def __repr__(self):
        return self.__data.__repr__()

    def __eq__(self, rhs):
        # return self.__data == rhs._get_data_struct
        return repr(self) == repr(rhs)

    def _walk(self, entrypoint, sep):
        entrypoints = [entrypoint]

        def is_dir(x):
            return x['type'] == _STANDARD_EXT.DIRECTORY_T

        while True:
            _entrypoint = entrypoints.pop(0)
            _dict_ptr = self.__get_file_dict(_entrypoint, sep=sep)

            keys = set(_dict_ptr['contents'].keys())
            _dirs = {key for key in keys if is_dir(_dict_ptr['contents'][key])}
            _files = keys - _dirs

            yield _entrypoint, _dirs, _files

            print(entrypoints)
            entrypoints.extend(
                [sep.join([_entrypoint, _dir]) for _dir in _dirs]
            )
            print(entrypoints)
            if not entrypoints:
                break

    def walk(self, entrypoint):
        os_type = self.__data['metadata']['system']['type']
        sep = ntsep if os_type == 'Windows' else posixsep

        return self._walk(entrypoint, sep)
