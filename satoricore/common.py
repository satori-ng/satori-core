from contextlib import contextmanager
import os
import imp
import sys

from satoricore.logger import logger


class _STANDARD_EXT(object):
    DIRECTORY_T = 'D'
    FILE_T = 'F'
    LINK_T = 'L'
    BLOCK_DEVICE_T = 'B'
    CHAR_DEVICE_T = 'C'
    FIFO_T = 'I'
    SOCKET_T = 'S'
    UNKNOWN_T = 'U'



@contextmanager
def dummy_context(obj):
    yield obj

def get_image_context_from_arg(arg, allow_local=True):
    from satoricore.file import load_image

    if arg == '.':
        os_obj = os
        expose(os_obj, os.path, 'isdir', target_name='is_dir')
        return dummy_context(os_obj)
    if allow_local:
        try:
            os.stat(arg)
            logger.info("Found to '{}'".format(arg))

            image_path = arg
            source = load_image(image_path)

            if source != None:
                return dummy_context(source)
        except FileNotFoundError:
            logger.error("File '{}' could not be found".format(arg))
            pass

    try:
        import satoriremote
        logger.info("Connecting to '{}'".format(arg))
        conn_context_source, conn_dict = satoriremote.connect(arg)
        logger.warn("Connected to {}".format(
                            conn_dict['host']
                        )
                    )
        return conn_context_source
        # with conn_context_source as context:
        #     return context
    except ImportError:
        logger.critical("'satori-remote' package not available, remote paths can't be used")
        sys.exit(-1)
    except ValueError:  # If can't be parsed as regular expression
        logger.critical("'{}' can't be parsed as URI".format(arg))
        sys.exit(-1)
    except ConnectionError:
        logger.critical("Connection failed for path '{}'".format(arg))
        sys.exit(-1)


def load_extension_list(extension_list):
    """
    extension_list: list of filenames 
    """
    for i, extension in enumerate(extension_list):
        try:
            ext_module = imp.load_source(
                'extension_{}'.format(i),
                extension
                )
            logger.warn("Extension '{}' loaded".format(ext_module.__name__))
        except Exception as e:
            logger.error(
                "[{}] - Extension {} could not be loaded".format(
                    e, extension
                )
            )


def expose(base, target, attr_name, target_name = None):
    attr = getattr(target, attr_name)
    if target_name == None:
        target_name = attr_name
    setattr(base, target_name, attr)

def expose_list(base, target, attr_list):
    for attr in attr_list:
        expose(base, target, attr)