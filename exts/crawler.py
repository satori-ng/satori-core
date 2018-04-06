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
from exts.common import ExtensionList

_extensions = {
        "on_start": ExtensionList(),
        "pre_open": ExtensionList(),
        "with_open": ExtensionList(),
        "post_close": ExtensionList(),
        "on_end": ExtensionList()
        }


def hook(key, deps=None):
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
    value = _extensions[key]
    if isinstance(value, ExtensionList) and \
            (deps is None or isinstance(deps, str) or isinstance(deps, list)):
        # In case @my_name(), @my_name('dependency') or
        # @my_name(['dep1', 'dep2']) is used
        def wrap(fn):
            fn.__deps__ = deps
            value.load(fn)
            return fn
        return wrap
    # TODO: Else exception maybe?
