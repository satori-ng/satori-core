#!/usr/bin/env python3

import argparse
from satoricore.crawler import BaseCrawler
from satoricore.image import SatoriImage


def _clone(args):
    crawler = BaseCrawler(args.entrypoints, args.excluded_dirs)
    image = SatoriImage()
    for filename, filetype, _ in crawler():
        image.add_file(filename, filetype)
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
        args.func(args)
