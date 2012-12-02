#!/usr/bin/env python

import os
import sys


class Scatter(object):
    def __init__(self):
        self.args = self.parse_args()
        self.site = self.get_site_to_deploy()
        self.deploys = self.get_deploy_root()

    def parse_args(self):
        num = len(sys.argv)

        if num == 1:
            return {}
        else:
            return {'site': sys.argv[1]}

    def get_deploy_dir(self):
        deploy_dir = self.deploys + self.site + os.sep

        if not os.path.isdir(deploy_dir):
            sys.exit("Deploy path doesn't exist: " + deploy_dir)

        return deploy_dir

    def get_site_to_deploy(self):
        if 'site' in self.args:
            return self.args.site
        else:
            return self.find_current_git_repo()

    def find_current_git_repo(self):
        # Bail if we are not in a git repo
        if not os.system('git rev-parse 2> /dev/null > /dev/null') == 0:
            sys.exit("We're not in a git repo")

        # Returns the path to the root of the current git repo
        current_git_root = os.popen('git rev-parse --show-toplevel').read().rstrip()
        return os.path.basename(current_git_root)

    def get_deploy_root(self):
        # Path to the root of the deploy scripts directory
        path = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'deploys'

        # Trailing slash
        return os.path.normpath(path) + os.sep

    def find_capfile(self, path):
        # Assumes finding a Capfile means this is a Capistrano site
        capfile = path + 'Capfile'

        if not os.path.isfile(capfile):
            return False
        else:
            return capfile





def get_deploy_routines(deploy_dir):
    custom = find_custom_deploy(deploy_dir)
    capfile = find_capfile(deploy_dir)

    return {'custom': custom, 'capfile': capfile}



def find_capfile(path):
    # Assumes finding a Capfile means this is a Capistrano site
    capfile = path + 'Capfile'

    if not os.path.isfile(capfile):
        return False
    else:
        return capfile


def find_custom_deploy(path):
    # Deploy should be executable and named without a file extension
    deploy = path + 'deploy'

    if not os.path.isfile(deploy):
        return False
    elif not os.access(deploy, os.X_OK):
        return False
    else:
        return deploy
