"""
Arcane Hook

I'm a hooker from Silvermoon City. Let me show you the Arcane way to Python
NOTE: Use me, use me haaaard...
Available hooking decorators:
    @hook("on_start") # Crawler has just started. Fasten your extension's seatbelt!
    @hook("pre_open") (passes `path=<path: str>`) # File is not open yet... a hard one ;)
    @hook("with_open") (passes `path=<path: str>, fd=<file descriptor: os.fd`) # File just opened, waiting for your kinky games
    @hook("post_close") (passes `path=<path: str>`) # File just came...
    @hook("on_end") # DEATH
"""
import collections

from exts.common import ExtensionList

_plugins = {
    "on_start": ExtensionList(),
    "pre_open": ExtensionList(),
    "with_open": ExtensionList(),
    "post_close": ExtensionList(),
    "on_end": ExtensionList()
}


def hook(key, dependencies=None):
    """
    Crawler hook. Usage:

    foo.py
        @hook("on_start")
        def bar():
            print("I'll be called when crawler starts!")

    test.py
        @hook("on_start", "foo")
        def foo():
            print("I'll be called when crawler starts, but after `foo` hooks!")

    anothertest.py
        @hook("with_open", "test")
        def foo(path, fd):
            print("Test module is already executed.")
            print("Currently processing file %s" % path)
    """
    extension_list = _plugins.get(key, None)
    if extension_list is None:
        raise Exception(
            'Invalid key provided. Valid options: %s' %
            ', '.join(_plugins.keys())
        )

    has_valid_dependencies = (
        dependencies is None or
        isinstance(dependencies, str) or
        isinstance(dependencies, collections.Iterable)
    )
    if not has_valid_dependencies:
        raise Exception('Invalid list of dependencies provided with `hook`')

    def wrapper(fn):
        fn.__deps__ = dependencies
        extension_list.load(fn)
        return fn
    return wrapper
