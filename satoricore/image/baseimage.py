import json
import os
import os.path
import re
import pathlib
import uuid
from satoricore.common import _STANDARD_EXT, expose, expose_list

from satoricore.image.filesystem import SatoriFileSystemImage

_DATA_SECTION = 'data'
_META_SECTION = 'metadata'

posixsep = pathlib.posixpath.sep
ntsep = pathlib.ntpath.sep


class SatoriImage(object):

    fs_exposed = [
        'add_file',
        'get_dir_contents',
        'get_attribute', 'set_attribute',
        'set_multiple_attributes',
        'is_dir', 'listdir',
        'lstat', 'stat',
    ]

    def __init__(self):
        self.__data = {}
        self.__data[_META_SECTION] = {}
        self.__data[_DATA_SECTION] = {}
        # ===== Create the Filesystem container
        self.__set_class_filesystem({})

        self.path = os.path     # helps with duck typing against 'os' module
        # Add a UUID in every single instance
        self.add_class('uuid', section=_META_SECTION, data=str(uuid.uuid4()))

    def get_entrypoints(self):
        return self.__data[_DATA_SECTION]['filesystem'].keys()

    def add_section(self, section_name):
        if section_name in self.__data:
            raise KeyError("The section '{}' already exists in Image"
                .format(
                    section_name,
                    )
                )
        self.__data[section_name] = {}

    def get_classes(self, section=_DATA_SECTION):
        if section not in self.__data:
            raise KeyError("The section '{}' does not exists in Image"
                .format(
                    section,
                    )
                )
        return self.__data[section].keys()

    def add_class(self, class_name, section=_DATA_SECTION, data={}):
        # if not isinstance(data, dict):
        #     raise TypeError("'data' parameter must be of type 'dict'")
        if class_name in self.__data[section]:
            raise KeyError("The class '{}' already exists in Section {}"
                .format(
                    class_name,
                    section,
                    )
                )
        self.__data[section][class_name] = data

    def get_class(self, class_name, section=_DATA_SECTION):
        if class_name not in self.__data[section]:
            raise KeyError("'{}' does not exist in Section '{}'"
                .format(
                class_name,
                section,
                )
            )
        return self.__data[section][class_name]

    def _get_data_struct(self):
        return self.__data

    def __set_class_filesystem(self, fs_dict):
        fs_image = SatoriFileSystemImage(
                init_dict=fs_dict
            )
        self.__data[_DATA_SECTION]['filesystem'] = fs_image
        expose_list(self, fs_image, self.fs_exposed)

    def _set_data_struct(self, data_struct):
        self.__data = data_struct
        self.__set_class_filesystem(data_struct[_DATA_SECTION]['filesystem'])

    def set_metadata(self, attr_dict, metadata_type):
        self.__data[_META_SECTION][metadata_type] = attr_dict

    def __str__(self):
        return json.dumps(self.__data)

    def __repr__(self):
        return self.__data.__repr__()

    def __eq__(self, rhs):
        # return self.__data == rhs._get_data_struct
        return repr(self) == repr(rhs)



    '''
from satoricore.file import load_image
im = load_image("bin_test_image.json.gz")
s = im.stat('/bin/bash')


    '''