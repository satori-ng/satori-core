import os
import os.path
import platform

from pprint import pprint

import satoricore

# Those tags will end up in the __data dict several times
# Here they can be globally minified
_TYPE_S = 'type'
_DIRECTORY_T = 'D'
_FILE_T = 'F'

_CONTENTS_S = 'contents'
_SIZE_S = 'filesize'

_STANDARD_EXT = [
    _CONTENTS_S,
    _SIZE_S,
    _TYPE_S,
]


class SatoriImage(object):

    def __init__(self, clone=data_dict):

        if data_dict:
            self.__data = clone
            return

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
        #     self.__data['metadata']['system']['specifics']['win'] = platform.win32_ver()
        # except :
        #     pass
        # try :
        #     self.__data['metadata']['system']['specifics']['mac'] = platform.mac_ver()
        # except :
        #     pass

    def add_file(self, full_path, type=_FILE_T):
        filedict = self.set_attribute(full_path, {}, _CONTENTS_S, force_create=True)
        filedict[_TYPE_S] = _FILE_T

    def set_attribute(self, full_path, attr_dict, ext_name, force_create=False):
        file_dict = self.__get_file_dict(full_path, force_create=force_create)
        if ext_name not in _STANDARD_EXT:
            self.__data['metadata']['satori']['extensions'].append(ext_name)
        file_dict[ext_name] = attr_dict
        return file_dict

    def __get_file_dict(self, full_path, force_create=False):
        if full_path.endswith('/'):
            full_path = full_path[:-1]
        # Get a list from the separated path
        path_tokens = full_path.split(os.sep)
        # clear the list from empty strings
        # path_tokens = [token for token in path_tokens if token]
        cur_position = self.__data['data']['filesystem']
        for token in path_tokens[:-1]:
            if force_create:
                try:
                    # Try Accessing directory contents
                    if _CONTENTS_S not in cur_position[token].keys():
                        raise NotADirectoryError("File: '{}' in Path: '{}' is not a Directory".format(token, full_path))
                    # cur_position[token][_CONTENTS_S]
                except KeyError:
                    # Directory doesn't exist - create it
                    cur_position[token] = {
                        _CONTENTS_S: {},
                        _TYPE_S: _DIRECTORY_T,
                    }
            cur_position = cur_position[token][_CONTENTS_S]
        # Create a file as an empty dict
        file_token = path_tokens[-1]
        if file_token not in cur_position.keys():
            cur_position[file_token] = {}
        return cur_position[file_token]

    def get_dir_contents(self, full_path):
        dir_dict = self.__get_file_dict(full_path)
        if _CONTENTS_S not in dir_dict.keys():
            raise FileNotFoundError("Does not exist: '{}'".format(full_path))
        if dir_dict[_TYPE_S] != _DIRECTORY_T:
            raise NotADirectoryError("Not a directory: '{}'".format(full_path))
        return dir_dict[_CONTENTS_S].keys()

    def _test_print(self, key=None):
        if key:
            pprint(self.__data[key])
        else:
            pprint(self.__data)


if __name__ == '__main__':
    si = SatoriImage()

    si.add_file('/')
    # si.add_file('/etc')
    si.add_file('/etc/passwd/')
    si.add_file('/dev/random')
    si.add_file('/etc/shadow')
    sres = os.stat('/etc/shadow')
    si.set_attribute('/etc/shadow', sres, 'stat')
    si.set_attribute('/etc/shadow', sres.st_size, _SIZE_S)
    # print si.__data
    si._test_print('data')

    print(si.get_dir_contents('/asas'))
