Arcane Hooker

I'm a hooker from Silvermoon City. Let me show you the Arcane way to Python
NOTE: Use me, use me haaaard...

This is my attempt to reinvent the hooking wheel.
I try to keep it simple for both providers and consumers.

The whole idea is that there are events, created by either the guts of the app
or an plugin itself on runtime.
After that, the required plugins that actually implemnt hooks on the events
should be imported. Example:

main.py
```
import hooker
hooker.EVENTS.append(["on_start", "with_open"])

import foo
import test
import anothertest
```

foo.py
```
@hook("on_start")
def bar():
	print("I'll be called when crawler starts!")
```

test.py
```
import hooker

@hook("on_start", "foo")
def foo():
	print("I'll be called when crawler starts, but after `foo` hooks!")
```

anothertest.py
```
@hook("with_open", "test")
def foo(path, fd):
	print("Test module is already executed.")
	print("Currently processing file %s" % path)
```
