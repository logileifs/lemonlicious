#!/usr/bin/python
import os
import sys
import time
import optparse
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

package = False
executable = None


class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        run_process()


def run_process():
    global process
    global executable
    try:
        process.terminate()
    except NameError as ne:
        pass
    except Exception as ex:
        print('could not terminate process - reason: %s' % ex)
    new_environ = os.environ.copy()
    rv = [sys.executable]
    if package:
        py_script = executable
        rv.append('-m')
    else:
        py_script = os.path.abspath(executable)
    rv.append(py_script)
    process = subprocess.Popen(
        rv,
        cwd=os.getcwd(),
        env=new_environ,
        close_fds=False
    )


def main():
    global package
    global executable
    parser = optparse.OptionParser()
    parser.add_option('-p', '--path', help='a path to watch', default='.')
    parser.add_option('-m', action="store_true", dest="package")
    opts, args = parser.parse_args()
    executable = args.pop()
    package = opts.package
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        run_process()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
