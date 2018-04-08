import inspect
import collections


class HookException(Exception):
    pass


class HookList(list):
    # If an extension is loaded before all its dependencies are loaded, put it
    # in this list and try to load it again after loading more extensions
    later = []

    def __call__(self, *args, **kwargs):
        if not self.later:
            raise HookException(
                "Dependencies not met for: %s" %
                [x.__name__ + ":" + x.__module__ for x in self.later])

        for fn in self:
            print('Calling %s from module %s with args: %s and kwargs: %s' %
                  (fn.__name__, fn.__module__, args, kwargs))
            # Skip extension if it doens't accept the arguments passed
            try:
                inspect.getcallargs(fn, *args, **kwargs)
            except TypeError:
                # TODO: Add logging for skipped extensions
                continue
            fn(*args, **kwargs)

    def isloaded(self, name):
        """Checks if given hook module has been loaded"""
        if name is None:
            return True
        if isinstance(name, collections.Iterable):
            return set(name).issubset(self)
        return name in [x.__module__ for x in self]

    def load(self, fn):
        """Tries to load a hook"""
        if self.isloaded(fn.__deps__):
            self.append(fn)
        else:
            self.later.append(fn)

        for ext in self.later:
            if self.isloaded(ext.__deps__):
                self.later.remove(ext)
                self.load(ext)
