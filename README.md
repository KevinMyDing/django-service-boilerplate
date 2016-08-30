[![Build Status](https://travis-ci.org/pahaz/django-project-stub.svg?branch=master)](https://travis-ci.org/pahaz/django-project-stub)

![index](./docs/img/index.png)

# HowTo Use #

  1. install `pip` -- https://pip.pypa.io/en/stable/installing/#installation
  1. install `virtualenv` -- https://virtualenv.pypa.io/en/stable/installation/#installation
  1. install `virtualenvwrapper` -- https://virtualenvwrapper.readthedocs.io/en/latest/install.html#installation
  1. install `invoke` -- http://www.pyinvoke.org/installing.html#installing

Frontend requirements:

  1. install `bower` -- https://bower.io/#install-bower

Create new virtual environment (if required):

    mkvirtualenv --python=python3.5 project-name

Create new project:

    git clone https://github.com/pahaz/django-project-stub.git project-name
    cd project-name
    inv init


# Project structure #

 - [dir] `__data__` - project media data (`venv`, `media` files, `db` files, `cache`, etc)
 - [dir] `_project_` - project level files
    - [dir] `./templates` - project common templates
    - [dir] `./static` - project common static files (js, css, img, etc)
    - [file] `./settings.py` - project settings
    - [file] `./urls.py` - project routs
 - [file] `requirements.txt` - project requirements
 - [file] `manage.py` - django manage file
 - [file] `tasks.py` - invoke manage file

# Tested #

OS: Windows/MacOS/Linux
Python: 3.5
