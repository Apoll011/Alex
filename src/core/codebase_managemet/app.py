import os
import subprocess
import sys
from getpass import getuser

def is_compiled():
    return getattr(sys, "frozen", False)

def restart_app():
    try:
        if is_compiled():
            executable = sys.executable

            subprocess.Popen([executable] + sys.argv[1:])
        else:
            python = sys.executable

            os.execv(python, [python] + sys.argv)
    except Exception as e:
        print(e)

def home():
    return f"/home/{getuser()}/"
