from fabric.api import local
import os

reganha = os.name == "nt"
RUNNING_IN_RPI = os.name == 'posix' and 'arm' in os.popen('uname -m').read()
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "IEEEISTwebsite")


# Do use this if you want to perform an action in virtualenv.
def run_in_venv(cmd):
    if reganha:
        local('venv\\Scripts\\activate && %s' % cmd)
    else:
        local('source .env/bin/activate && %s' % cmd, shell='/bin/bash')


def setup():
    # set up virtualenv
    if not ("venv" in os.listdir('.')):
        local('sudo pip install virtualenv')
        local('virtualenv venv')

    # install packages if necessary
    packages = ['libmysqlclient-dev', 'mysql-server-5', 'python-dev']
    for p in packages:
        if p == packages[1]:
            p += '.6'
        if ' ' + p + ' ' in local('dpkg -l', capture=True):
            print "\"" + p + "\"" + " is already installed on this machine"
        else:
            local('sudo apt-get install ' + p)

    run_in_venv('pip install -r requirements.txt')
    initdb()
    migrations()
    print "Setup successfully done"


def update_requirements():
    run_in_venv('pip install -r requirements.txt')


def freeze():
    run_in_venv('pip freeze > requirements.txt')


def run_local(port=8000):
    run_in_venv('python manage.py runserver %s' % port)


def run_ip(ip):
    run_in_venv('python manage.py runserver %s:8000' % ip)


def migrations():
    makemigrations()
    migrate()


def makemigrations():
    run_in_venv('python manage.py makemigrations')


def migrate():
    run_in_venv('python manage.py migrate')


def initdb():
    local("mysql -u root < deploy/init.sql")


def cleandb():
    if RUNNING_IN_RPI:
        local("rm " + os.path.join(BASE_DIR, "ieee.sqlite3"))
    else:
        local("mysql -u ieeeist -pieeeistdb -e \"DROP DATABASE IF EXISTS ieee_ist_db\"")
        local("mysql -u ieeeist -pieeeistdb -e \"CREATE DATABASE IF NOT EXISTS ieee_ist_db\"")


def delete_migrations():
    local("rm -f app/migrations/0*")


def cleandbmigrate():
    cleandb()
    delete_migrations()
    migrations()


def pull_r():
    local('git pull --rebase origin master')


def commit(msg):
    # fab commit:"msg"
    if msg[0] == '"':
        msg = msg[1:]
    if msg[-1] == '"':
        msg = msg[:-1]

    local('git add --all')
    local('git commit -m \"' + msg + '\"')


def push():
    local('git push origin master')


def git_all(msg):
    commit(msg)
    pull_r()
    push()


def fix_merge():
    local('git add --all')
    local('git rebase --continue')


def mktrans():
    run_in_venv('python manage.py makemessages -l pt -i venv -i app/templates/admin')


def cmpltrans():
    run_in_venv('python manage.py compilemessages -l pt')


def cleanthisshit():
    if not reganha:
        local('rm -rf media/img')
    cleandb()
    migrate()
    run_in_venv('python manage.py initdb')


def shell():
    run_in_venv('python ./manage.py shell')
