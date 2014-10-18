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
./manage.py migrate
```

## Usage

```bash
cd /path/to/halalar-web/halalar
workon halalar
./manage.py runserver 0.0.0.0:8000
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

## Restoring

```bash
fab restore
```