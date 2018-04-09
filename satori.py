#!/usr/bin/env python3

import argparse
from satoricore.crawler import BaseCrawler
from satoricore.hooker import EVENTS
from satoricore.image import SatoriImage

EVENTS.append(["on_start", "pre_open", "with_open", "post_close", "on_end"])


def _clone(args):
    crawler = BaseCrawler(args.entrypoints, args.excluded_dirs)
    image = SatoriImage()

    for filename, filetype in crawler():
        image.add_file(filename, filetype)
        EVENTS["pre_open"](satori_image=image, file_path=filename, file_type=filetype)
        fd = open(filename)
        EVENTS["with_open"](satori_image=image, file_path=filename, file_type=filetype, fd=fd)
        fd.close()
        EVENTS["post_close"](satori_image=image, file_path=filename, file_type=filetype)

    image._test_print()


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
        'entrypoints',
        help='Start iteration using these directories.',
        nargs='+',
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
