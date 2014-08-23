from fabric.api import cd, env, local, prefix, run, sudo

env.hosts = ['halalar.com:12345']

def test():
    local('python manage.py test marketing.tests legal.tests')

def style():
    local('flake8 .')

def deploy():
    with cd('/srv/halalar-web'):
        run('git pull')

        with prefix('workon halalar'):
            run('pip install -r requirements.txt')

            with cd('halalar'):
                run('python manage.py syncdb --noinput')
                run('python manage.py collectstatic --noinput')

    sudo('service halalar restart')
    sudo('service nginx restart')