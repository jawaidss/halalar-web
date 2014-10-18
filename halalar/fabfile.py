from fabric.api import cd, env, local, prefix, run, sudo

env.hosts = ['halalar.com:12345']

def test():
    local('./manage.py test marketing.tests legal.tests api.tests')

def style():
    local('flake8 . --ignore=E261,W292,E302,E501')

def deploy():
    with cd('/srv/halalar-web'):
        run('git pull')

        with prefix('workon halalar'):
            run('pip install -r requirements.txt')

            with cd('halalar'):
                run('./manage.py migrate --noinput')
                run('./manage.py collectstatic --noinput')

    sudo('service halalar restart')
    sudo('service nginx restart')

def restore():
    local('./manage.py runscript restore')
    local('./manage.py set_fake_passwords --password=temp123')