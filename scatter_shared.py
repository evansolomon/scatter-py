#!/usr/bin/env python

import os
import sys


def get_deploy_routines(deploy_dir):
    custom = find_custom_deploy(deploy_dir)
    capfile = find_capfile(deploy_dir)

    return {'custom': custom, 'capfile': capfile}


def get_deploy_dir(cap=False):
    site = get_site_to_deploy(cap)
    deploy_root = get_deploy_root()

    # Make sure the deploy path exists
    deploy_dir = deploy_root + site + os.sep
    if not os.path.isdir(deploy_dir):
        sys.exit("Deploy path doesn't exist: " + deploy_dir)

    return deploy_dir


def get_site_to_deploy(cap):
    # Optionally pass the site to deploy as an argument
    if len(sys.argv) > 1 and sys.argv[1] and not cap:
        return sys.argv[1]
    else:
        return find_current_git_repo()


def find_current_git_repo():
    # Bail if we are not in a git repo
    if not os.system('git rev-parse 2> /dev/null > /dev/null') == 0:
        sys.exit("We're not in a git repo")

    # Returns the path to the root of the current git repo
    current_git_root = os.popen('git rev-parse --show-toplevel').read().rstrip()
    return os.path.basename(current_git_root)


def get_deploy_root():
    # Path to the root of the deploy scripts directory
    default = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'deploys'

    # Optionally pass a deploy directory as an argument
    if len(sys.argv) > 2 and sys.argv[2]:
        path = find_custom_deploys_root(sys.argv[2], default)
    else:
        path = default

    # Trailing slash
    return os.path.normpath(path) + os.sep


def find_custom_deploys_root(path, default):
    # 'path' can be a full path or relative to the deploys dir
    if os.path.isdir(path):
        return path
    elif os.path.isdir(default + path):
        return default + path
    else:
        sys.exit('Invalid path: ' + path)


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
