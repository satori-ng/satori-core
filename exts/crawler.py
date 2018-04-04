"""
# Crawler extensions

Please do not open or close system files for scanning.
Do that with hooking!
"""
import exts.common

_plugins = {
        "on_start": exts.common.PluginList(),
        "pre_open": exts.common.PluginList(),
        "with_open": exts.common.PluginList(),
        "post_close": exts.common.PluginList(),
        "on_end": exts.common.PluginList()
        }


def _add_plugin(func, at):
    _plugins[at].append(func)


def on_start(fn):
    """Function wiil be called when the crawler starts"""
    _add_plugin(fn, "on_start")
    return fn


def pre_open(fn):
    """Function wiil be called BEFORE the file is opened"""
    _add_plugin(fn, "pre_open")
    return fn


def with_open(fn):
    """Function wiil be called while the file is opened"""
    _add_plugin(fn, "with_open")
    return fn


def post_close(fn):
    """Function wiil be called after the file is closed"""
    _add_plugin(fn, "post_close")
    return fn


def on_end(fn):
    """Function wiil be called when the crawler ends"""
    _add_plugin(fn, "on_end")
    return fn
