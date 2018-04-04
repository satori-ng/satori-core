class PluginList(list):
    def __call__(self, *args, **kwargs):
        for fn in self:
            print('Calling %s from module %s with args: %s and kwargs: %s' % (fn.__name__, fn.__module__, args, kwargs))
            fn(*args, **kwargs)
