# coding=utf-8
from __future__ import unicode_literals
from __future__ import print_function

import subprocess
import shutil
import stat
import sys
import os
from tempfile import NamedTemporaryFile
from os.path import dirname, join, abspath, basename

__author__ = 'pahaz'
# located in <project_root>/<some_dir-aka-helpers>/lib.py
_root = abspath(dirname(dirname(__file__)))


def fix_sys_paths():
    if hasattr(fix_sys_paths, "path_fixed"):
        return
    # insert stub root for import paths
    sys.path.insert(1, _root)
    setattr(fix_sys_paths, "path_fixed", True)


def root_join(*args):
    return join(_root, *args)


def import_project_stub_settings(path):
    __import__(path)
    return sys.modules[path]


def fake_project_stub_settings(PROJECT_DIR_NAME="_project_"):
    ROOT_DIR = _root
    ROOT_DIR_NAME = basename(ROOT_DIR)

    PROJECT_DIR = join(ROOT_DIR, PROJECT_DIR_NAME)
    PROJECT_DIR_NAME = basename(PROJECT_DIR)

    PATH_TO_PROJECT_VENV_DIR = join(ROOT_DIR, '__data__', 'venv')
    PATH_TO_PROJECT_LOG_DIR = join(ROOT_DIR, '__data__', 'log')
    PATH_TO_PROJECT_COLLECT_STATIC_DIR = \
        join(ROOT_DIR, '__data__', 'collected_static')
    PATH_TO_PROJECT_MEDIA_DIR = join(ROOT_DIR, '__data__', 'media')
    PATH_TO_PROJECT_TMP_DIR = join(ROOT_DIR, '__data__', 'tmp')
    PATH_TO_PROJECT_SQLITE_FILE = join(ROOT_DIR, '__data__', 'db.sqlite')
    PATH_TO_PROJECT_REQUIREMENTS_FILE = join(ROOT_DIR, 'requirements.txt')

    PATH_TO_PROJECT_DATA_DIR = join(ROOT_DIR, '__data__')

    settings = object()
    settings.ROOT_DIR = ROOT_DIR
    settings.ROOT_DIR_NAME = ROOT_DIR_NAME
    settings.PROJECT_DIR = PROJECT_DIR
    settings.PROJECT_DIR_NAME = PROJECT_DIR_NAME
    settings.PATH_TO_PROJECT_VENV_DIR = PATH_TO_PROJECT_VENV_DIR
    settings.PATH_TO_PROJECT_LOG_DIR = PATH_TO_PROJECT_LOG_DIR
    settings.PATH_TO_PROJECT_COLLECT_STATIC_DIR = \
        PATH_TO_PROJECT_COLLECT_STATIC_DIR
    settings.PATH_TO_PROJECT_MEDIA_DIR = PATH_TO_PROJECT_MEDIA_DIR
    settings.PATH_TO_PROJECT_TMP_DIR = PATH_TO_PROJECT_TMP_DIR
    settings.PATH_TO_PROJECT_SQLITE_FILE = PATH_TO_PROJECT_SQLITE_FILE
    settings.PATH_TO_PROJECT_REQUIREMENTS_FILE = \
        PATH_TO_PROJECT_REQUIREMENTS_FILE
    settings.PATH_TO_PROJECT_DATA_DIR = PATH_TO_PROJECT_DATA_DIR
    settings._stub_settings_version_ = '0.0.1'
    return settings

def is_venv_exists(settings):
    active_file = venv_script_file(settings, "activate")
    return os.path.exists(active_file)


def venv_pip_file(settings):
    return venv_script_file(settings, 'pip')


def venv_python_file(settings):
    return venv_script_file(settings, 'python')


def venv_script_file(settings, filename):
    bin_ = 'Scripts' if sys.platform == 'win32' else 'bin'
    return join(settings.PATH_TO_PROJECT_VENV_DIR, bin_, filename)


def venv_activate_command(settings):
    active = venv_script_file(settings, "activate")
    active = active if sys.platform == 'win32' else 'source ' + active
    return active


def pip_install(pip, requirements_file, use_cache=True, cache_dir=None):
    command = [pip, 'install']
    if use_cache:
        if not cache_dir:
            cache_dir = join(_root, '..', '.pip_cache')
        command.append('--download-cache={0}'.format(cache_dir))
    command.extend(['-r', requirements_file])
    subprocess.call(command)


def separate_requirements(settings):
    req_file = settings.PATH_TO_PROJECT_REQUIREMENTS_FILE
    common_req = []
    dev_req = []
    with open(req_file, 'r') as f:
        reqs = iter(f.readlines())
        for x in reqs:
            if x.upper().startswith("# DEV"):
                dev_req.append(x)
                break
            common_req.append(x)

        for x in reqs:
            dev_req.append(x)
    return {'common': common_req, 'dev': dev_req}


def separate_requirements_as_files(settings):
    req = separate_requirements(settings)
    req_common = ''.join(req['common'])
    req_dev = ''.join(req['dev'])
    req_common_file = make_temp_file(req_common)
    req_dev_file = make_temp_file(req_dev)
    return {'common': req_common_file, 'dev': req_dev_file,
            'common_content': req_common, 'dev_content': req_dev}


def make_temp_file(content):
    common = NamedTemporaryFile('w', delete=False)
    common.write(content)
    common.close()
    return common.name


def make_dir_if_not_exists(path):
    path = path.rstrip('/')
    if not os.path.exists(path):
        base = os.path.dirname(path)
        make_dir_if_not_exists(base)
        os.mkdir(path)
        return True
    return False


def rm_file(*paths):
    f_path = root_join(*paths)
    if os.path.exists(f_path) and os.path.isfile(f_path):
        os.remove(f_path)


def rm_dir(*paths):
    def _on_rm_error(func, path, exc_info):
        # path contains the path of the file that couldn't be removed
        # let's just assume that it's read-only and unlink it.
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)

    f_path = root_join(*paths)
    if os.path.exists(f_path) and os.path.isdir(f_path):
        shutil.rmtree(f_path, onerror=_on_rm_error)