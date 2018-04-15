from setuptools import setup

import satoricore

setup(
    name=satoricore.__name__,
    description=satoricore.__desc__,
    version=satoricore.__version__,

    author="Satori-NG org",
    author_email=satoricore.__email__,

    packages=["satoricore"],

    # entry_points={
    #     "console_scripts": [
    #         "hexwordify=hexwordify.__main__:main",
    #     ],
    # },
)
