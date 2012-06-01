from __future__ import with_statement

import time
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['bjb.io:23']

def pull():
    local('git pull origin')

def build():
    local('make build')

def deploy(clean=False):
    timestamp = time.time()
    path = '/srv/www/eg-site-build.%s' % timestamp
    
    pull()
    build()
    
    local('scp -r _build bjb.io:%s' % (path,))
    
    with cd('/srv/www/'):
        if clean:
            run('mv %s eg-site-build.latest' % (path,))
            run('ln -f -s /srv/www/eg-site-build.latest eg.bjb.io')
            run('rm -r eg-site-build.1*')
            run('mv eg-site-build.latest %s' % (path,))
        run('ln -f -s %s eg.bjb.io' % (path,))
