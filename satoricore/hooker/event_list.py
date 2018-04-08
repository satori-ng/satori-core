from collections import Iterable

from satoricore.hooker.hook_list import HookList


class EventException(Exception):
    """An event threw up!"""
    pass


class EventList():
    """A list that holds all the events, each of which hold all hooks"""
    _events = {}

    def append(self, event):
        """Creates a new event. `event` may be iterable or string"""
        if isinstance(event, str):
            self._events[event] = HookList()
            return

        if isinstance(event, Iterable):
            for name in event:
                self.append(name)
            return

        raise EventException("De hell did you give me as an event name? O.o")

    def hook(self, event, function, dependencies=None):
        """Tries to load the hook to the event"""

        event_list = self._events.get(event, None)
        if event_list is None:
            raise EventException("Invalid key provided. Valid options: %s" %
                                 ", ".join(self._events.keys()))
        event_list.hook(function, dependencies)