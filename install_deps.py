#!/usr/bin/python
import sys
import subprocess

if sys.version_info[:2] < (2, 7):
    subprocess.call('pip install unittest2 --use-mirrors', shell=True)
