#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals
from __future__ import print_function

import subprocess
import sys
from tempfile import NamedTemporaryFile

from _settings import settings, root_join
from lib import venv_pip_install, venv_activate_command, \
    separate_requirements, rm_file, mkdir_if_not_exists


__author__ = 'pahaz'


def python_version(number):
    if number not in [2, 3]:
        raise RuntimeError('Only 2 or 3 python version support.')

    if sys.platform == 'win32':
        return 'C:\Python34\python.exe' if number == 3 else \
            'C:\Python27\python.exe'
    else:
        return 'python3' if number == 3 else 'python2'


if __name__ == "__main__":
    PRODUCTION_MODE = False
    PIP_CACHE_DIR = root_join('..', '.cache')
    USE_FIXES = False
    PY_VERSION = 3

    if '--production' in sys.argv:
        PRODUCTION_MODE = True

    print("\nMAKE VIRTUALENV\n")
    subprocess.call(['virtualenv', '--python=' + python_version(PY_VERSION),
                     '--no-site-packages', 
                     '--always-copy', 
                     settings.PATH_TO_PROJECT_VENV_DIR])

    is_made = mkdir_if_not_exists(PIP_CACHE_DIR)
    if is_made:
        print("\n MADE PIP CACHE DIR\n")

    print("\nINSTALL REQUIREMENTS\n")

    req = separate_requirements(settings)

    common_req = req['common']
    common_text = ''.join(common_req)
    dev_req = req['dev']
    dev_text = ''.join(dev_req)

    print("\n# ! #\n# COMMON requirements:\n\n\n" + common_text)
    print("\n# ! #\n# DEV requirements:\n\n\n" + dev_text)

    common = NamedTemporaryFile('w', delete=False)
    dev = NamedTemporaryFile('w', delete=False)
    common.write(common_text)
    dev.write(dev_text)
    common.close()
    dev.close()

    print("\nINSTALL COMMON\n")
    venv_pip_install(settings, common.name, PIP_CACHE_DIR)
    if not PRODUCTION_MODE:
        print("\nINSTALL DEV\n")
        venv_pip_install(settings, dev.name, PIP_CACHE_DIR)

    print("""NOW ACTIVATE:
     * {help_activate_venv}
    """.format(help_activate_venv=venv_activate_command(settings)))

    rm_file(common.name)
    rm_file(dev.name)
