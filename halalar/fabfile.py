from fabric.api import cd, env, local, prefix, run, sudo

env.hosts = ['halalar.com:12345']

def test():
    local('python manage.py test marketing.tests legal.tests api.tests')

def style():
    local('flake8 . --ignore=E261,W292,E302,E501')

def deploy():
    with cd('/srv/halalar-web'):
        run('git pull')

        with prefix('workon halalar'):
            run('pip install -r requirements.txt')

            with cd('halalar'):
                run('python manage.py migrate --noinput')
                run('python manage.py collectstatic --noinput')

    sudo('service halalar restart')
    sudo('service nginx restart')