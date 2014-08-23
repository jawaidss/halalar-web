# halalar-web

## Requirements

* [git](http://www.git-scm.com/)
* [virtualenv](http://www.virtualenv.org/)
* [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/)
* [pip](http://www.pip-installer.org/)
* [PostgreSQL](http://www.postgresql.org/)

## Installation

```bash
git clone git@github.com:jawaidss/halalar-web.git
cd halalar-web
mkvirtualenv halalar
pip install -r requirements.txt
sudo su postgres -c "createdb halalar"
sudo su postgres -c "createuser -P halalar"
sudo su postgres -c 'psql -c "ALTER USER halalar CREATEDB;"'
sudo su postgres -c 'psql -c "GRANT ALL PRIVILEGES ON DATABASE halalar TO halalar;"'
cd halalar
python manage.py syncdb --noinput
```

## Usage

```bash
cd /path/to/halalar-web/halalar
workon halalar
python manage.py runserver
```

## Testing

```bash
fab test
```

## Style

```bash
fab style
```

## Deploying

```bash
fab deploy
```