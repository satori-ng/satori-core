"""
Arcane Hooker

I'm a hooker from Silvermoon City. Let me show you the Arcane way to Python
NOTE: Use me, use me haaaard...

This is my attempt to reinvent the hooking wheel.
I try to keep it simple for both providers and consumers.

The whole idea is that there events, created by the guts of the app
by `_events["my_event_name"] = EventList()` on runtime.
Then, the required plugins/addons/extensions/potatomonkeys are imported
and actually hook on the created event(s).
For more info on how to do that, check the `hook` method.
"""
import collections

from satoricore.hooker.common import EventList

_events = {
    "on_start": EventList(),
    "pre_open": EventList(),
    "with_open": EventList(),
    "post_close": EventList(),
    "on_end": EventList()
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
    event_list = _events.get(key, None)
    if event_list is None:
        raise Exception(
            'Invalid key provided. Valid options: %s' %
            ', '.join(_events.keys())
        )

    has_valid_dependencies = (
        dependencies is None or
        isinstance(dependencies, (collections.Iterable, str))
    )
    if not has_valid_dependencies:
        raise Exception('Invalid list of dependencies provided with `hook`')

    def wrapper(fn):
        fn.__deps__ = dependencies
        event_list.load(fn)
        return fn
    return wrapper
