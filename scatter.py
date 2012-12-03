#!/usr/bin/env python

import os


class Scatter(object):
    def __init__(self, args):
        self.args = self.parse_args(args)
        self.site = self.get_site_to_deploy()
        self.deploys = self.get_deploy_root()

    def parse_args(self, args):
        return {'site': args[0]} if len(args) else {}

    def get_deploy_dir(self):
        deploy_dir = self.trailing_slash(self.deploys + self.site)
        return deploy_dir if os.path.isdir(deploy_dir) else False

    def get_site_to_deploy(self):
        if 'site' in self.args:
            return self.args['site']
        else:
            return self.find_current_git_repo()

    def find_current_git_repo(self):
        # Bail if we are not in a git repo
        if not os.system('git rev-parse 2> /dev/null > /dev/null') == 0:
            return False

        # Returns the path to the root of the current git repo
        current_git_root = os.popen('git rev-parse --show-toplevel').read().rstrip()
        return os.path.basename(current_git_root)

    def get_deploy_root(self):
        # Path to the root of the deploy scripts directory
        scatter = os.path.dirname(os.path.realpath(__file__))
        deploys = self.trailing_slash(scatter) + 'deploys'

        # Trailing slash
        return self.trailing_slash(os.path.normpath(deploys))

    def find_capfile(self, path):
        # Assumes finding a Capfile means this is a Capistrano site
        capfile = path + 'Capfile'
        return capfile if os.path.isfile(capfile) else False

    def trailing_slash(self, string):
        if os.sep == string[-1]:
            return string

        return string + os.sep
