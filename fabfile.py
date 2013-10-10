from fabric.api import env, run, sudo, cd, task

env.hosts = ['core.fort']
env.user = 'fort'
DEPLOY_PATH = "/data/projects/readfast"

@task(default=True)
def deploy():
    with cd(DEPLOY_PATH):
        run("git pull -q");
        run("venv/bin/python manage.py syncdb --migrate")
        #run("venv/bin/python manage.py collectstatic --noinput")
        run("node_modules/.bin/wake")
        sudo("service readfast restart")

