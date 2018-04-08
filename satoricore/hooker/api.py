from satoricore.hooker.event_list import EventList

EVENTS = EventList()
# events.append(["on_start", "pre_open", "with_open", "post_close", "on_end"])


def hook(event, dependencies=None):
    """Hooking decorator. Just `@hook(event, dependencies) on your function`"""

    def wrapper(func):
        """I'm a simple wrapper that manages event hooking"""
        func.__deps__ = dependencies
        EVENTS.hook(event, func, dependencies)
        return func
    return wrapper
