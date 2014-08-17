# halalar-web

## Requirements

* [git](http://www.git-scm.com/)
* [virtualenv](http://www.virtualenv.org/)
* [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/)
* [pip](http://www.pip-installer.org/)

## Installation

```bash
git clone git@github.com:jawaidss/halalar-web.git
cd halalar-web
mkvirtualenv halalar
pip install -r requirements.txt
```

## Usage

```bash
cd /path/to/halalar-web/halalar
workon halalar
python manage.py runserver
```