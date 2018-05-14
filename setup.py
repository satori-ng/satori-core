from setuptools import setup

import satoricore

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name=satoricore.__name__,
    description=satoricore.__desc__,
    version=satoricore.__version__,
    url=satoricore.__url__,

    author="Satori-NG org",
    author_email=satoricore.__email__,

    packages=[
        "satoricore",
        "satoricore.file",
        "satoricore.crawler",
        "satoricore.extensions",
    ],

    entry_points={
        "console_scripts": [
            "satori-file=satoricore.file.__main__:main",
        ],
    },
    install_requires=requirements,

)


