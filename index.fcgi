#!/usr/bin/python

# this code mostly from 6.170

import os, time, sys
try:
    import thread
except ImportError:
    pass

import threading
from flup.server.fcgi import WSGIServer
from main import app

_mtimes = {}
def code_changed(): # lovingly stolen from django. See above.
    global _mtimes
    names = sys.modules.values()
    for filename in filter(lambda v: v, map(lambda m: getattr(m, "__file__", None), names)):
        if filename.endswith(".pyc") or filename.endswith(".pyo"):
            filename = filename[:-1]
        if filename.endswith("$py.class"):
            filename = filename[:-9] + ".py"
        if not os.path.exists(filename):
            continue # File might be in an egg, so it can't be reloaded.
        stat = os.stat(filename)
        mtime = stat.st_mtime
        if filename not in _mtimes:
            _mtimes[filename] = mtime
            continue
        if mtime != _mtimes[filename]:
            _mtimes = {}
            return True
    return False
def reload_on_edit():
    while True:
        if code_changed():
            os._exit(5)
        else:
            time.sleep(1)


if __name__ == '__main__':
    t = threading.Thread(target=reload_on_edit)
    t.daemon = True
    t.start()
    WSGIServer(app).run()
