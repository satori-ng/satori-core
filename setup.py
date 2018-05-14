from setuptools import setup

import satoriremote

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name=satoriremote.__name__,
    description=satoriremote.__desc__,
    version=satoriremote.__version__,

    author="Satori-NG org",
    author_email=satoriremote.__email__,

    packages=["satoriremote"],

    entry_points={
        "console_scripts": [
            "satori-remote=satoriremote.__main__:main",
        ],
    },
    install_requires=requirements,

)

# python -m unittest discover tests