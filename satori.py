#!/usr/bin/env python3

import argparse
import os
import sys

from satoricore.hooker import EVENTS
EVENTS.append(["on_start", "pre_open", "with_open", "post_close", "on_end"])

from satoricore.crawler import BaseCrawler
from satoricore.image import SatoriImage
from satoricore.common import _STANDARD_EXT as SE

from satoricore.serialize.pickle import SatoriPickler
from satoricore.serialize.json import SatoriJsoner

from satoricore.hooker.defaults import *


def _clone(args):
    crawler = BaseCrawler(args.entrypoints, args.excluded_dirs)
    image = SatoriImage()
    if args.load_extensions:
        os.chdir("satoricore" + os.sep + "hooker" + os.sep + "defaults")


    for filename, filetype in crawler():
        image.add_file(filename)
        EVENTS["pre_open"](satori_image=image, file_path=filename, file_type=filetype)
        if filetype is not SE.DIRECTORY_T:
            try:
                fd = open(filename)
                EVENTS["with_open"](satori_image=image, file_path=filename, file_type=filetype, fd=fd)
                fd.close()
                EVENTS["post_close"](satori_image=image, file_path=filename, file_type=filetype)
            except Exception as e:
                if not args.quiet:
                    print("[-] %s . File '%s' could not be opened." % (e, filename), file=sys.stderr)
                # print(
                #     "[-] %s.  File '%s' could not be opened. " % (str(e), filename),
                #     file=sys.stdout,
                #     )

    # image_serializer = SatoriPickler(compress=False)
    image_serializer = SatoriJsoner()
    image_serializer.write(image, args.image_file)
    print("[+] Stored to file '{}'".format(image_serializer.last_file))

def _diff(args):
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
    )

    clone_parser.add_argument(
        '-q', '--quiet',
        help=("Does not show Errors"),
        default=False,
        action='store_true',
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
    if 'func' in args:
        EVENTS["on_start"](parser=parser, args=args)
        args.func(args)
        EVENTS["on_end"]()
