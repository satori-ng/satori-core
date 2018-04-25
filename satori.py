#!/usr/bin/env python3

import argparse
import imp
import itertools
import os
import os.path
import sys
from multiprocessing.dummy import Pool
# from multiprocessing import Pool

from hooker import EVENTS
EVENTS.append(["imager.on_start", "imager.pre_open", "imager.with_open", "imager.post_close", "imager.on_end"])

from satoricore.crawler import BaseCrawler
from satoricore.image import SatoriImage
from satoricore.common import _STANDARD_EXT as SE

from satoricore.serialize.pickle import SatoriPickler
from satoricore.serialize.json import SatoriJsoner

from satoricore.extensions import *


PROCESSED_FILES = 0


def file_worker(image, file_desc):
    global PROCESSED_FILES
    PROCESSED_FILES += 1
    filename, filetype = file_desc
    image.add_file(filename)
    EVENTS["imager.pre_open"](satori_image=image, file_path=filename, file_type=filetype)
    if filetype is not SE.DIRECTORY_T:
        # print (image)
        if len(EVENTS["imager.with_open"]):
            try:
                fd = open(filename, 'rb')
                EVENTS["imager.with_open"](satori_image=image, file_path=filename, file_type=filetype, fd=fd)
                fd.close()
                EVENTS["imager.post_close"](satori_image=image, file_path=filename, file_type=filetype)
            except Exception as e:
                if not args.quiet:
                    print("[-] %s . File '%s' could not be opened." % (e, filename), file=sys.stderr)
                # print(
                #     "[-] %s.  File '%s' could not be opened. " % (str(e), filename),
                #     file=sys.stdout,
                #     )


def _clone(args, image):
    entrypoints = []
    for entrypoint in args.entrypoints:
        if os.path.isdir(entrypoint):
            entrypoints.append(entrypoint)
        else:
            print ("[-] Entrypoint '{}' is not a Directory".format(entrypoint))
    if not entrypoints:
        print ("[!] No valid Entrypoints Found!")
        print ("[!] Exiting...")
        sys.exit(-1)
    crawler = BaseCrawler(entrypoints, args.excluded_dirs)
    # dispatcher(image, file_queue)
    for i, extension in enumerate(args.load_extensions):
        try:
            ext_module = imp.load_source(
                'extension_{}'.format(i),
                extension
                )
            print("Extension '{}' loaded".format(ext_module.__name__))
        except Exception as e:
            print ("[-] [{}] - Extension {} could not be loaded".format(e, extension))
    # os.chdir("satoricore" + os.sep + "hooker" + os.sep + "defaults")
    pool = Pool(args.threads) 
    pool.starmap(file_worker,       # image, filename, filetype
                zip(
                    itertools.repeat(image),
                    crawler(),
                )
            )
    pool.close()
    pool.join()

    print ("[*] Processed {} files".format(PROCESSED_FILES))
    print("[+] Image Generated!")
    # image_serializer = SatoriPickler(compress=False)
    image_serializer = SatoriJsoner()
    image_serializer.write(image, args.image_file)
    print("[+] Stored to file '{}'".format(image_serializer.last_file))

def _diff(args, image):
    raise NotImplementedError


def _setup_argument_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        help='Satori may run in either clone or diff modes.'
    )

    clone_parser = subparsers.add_parser(
        'clone',
        help=(
            'Generates an image file containing metadata for each file in the '
            'specified paths.'
        ),
    )

    clone_parser.add_argument(
        '-e', '--excluded-dirs',
        help='Exclude files under specified locations.',
        action='append',
    )

    clone_parser.add_argument(
        '-l', '--load-extensions',
        help='Load the following extensions',
        action='append',
        default=[],
    )

    clone_parser.add_argument(
        '-q', '--quiet',
        help=("Does not show Errors"),
        default=False,
        action='store_true',
    )

    clone_parser.add_argument(
        '-t', '--threads',
        help=("Number of threads to use"),
        default=4,
        type=int,
    )

    clone_parser.add_argument(
        'entrypoints',
        help='Start iteration using these directories.',
        nargs='+',
    )

    clone_parser.add_argument(
        'image_file',
        help='Store the created image in that file',
        default="%s.str" % os.uname,
    )

    clone_parser.set_defaults(func=_clone)

    diff_parser = subparsers.add_parser('diff')
    diff_parser.set_defaults(func=_diff)
    return parser


if __name__ == '__main__':
    parser = _setup_argument_parser()
    args = parser.parse_args()
    image = SatoriImage()
    if 'func' in args:
        EVENTS["imager.on_start"](parser=parser, args=args, satori_image=image)
        args.func(args, image)
        EVENTS["imager.on_end"]()
