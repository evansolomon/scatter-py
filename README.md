# Scatter

This is a command line tool I wrote to help manage deploying different projects.  It comes with two commands, `scatter` (used for deploys) and `scap` (used for proxying capistrano commands to deploy directories).

It is strongly influenced by our deploy script on WordPress.com, which I like quite a bit.  It was written entirely for my own use, but I figured someone else might find it valuable.

## Installation

Since scatter is meant to be used on the command line, it requires some command line setup.  First, clone this repository.

`git clone https://github.com/evansolomon/scatter.git`

To make Scatter useful, you will need access to its command in your `PATH`.  I like to symlink them to a common directory that I use for bin scripts.

`ln -nfs $PWD/scatter/scatter /path/to/bin/scatter`
`ln -nfs $PWD/scatter/scap /path/to/bin/scap`

If you want, you can rename the script to whatever you choose like this.

`ln -nfs $PWD/scatter/scatter /path/to/bin/notscatter`

## Usage

### Scatter's Assumptions
Now that you have Scatter installed, you'll need to setup some deploy scripts for it to use.  By default, Scatter looks for deploy scripts in its install directory (the place you `git clone`'d it, not the symlink target), in a subdirectory called `deploys`.  The default behavior expects deploy files in a directory like `/path/to/scatter/deploys/project-name/`.  The `deploys` directory is intentionally `gitignore`'d so that you can put your own directory there without conflict.

### Deploy Routines
Scatter looks for two flavors of deploy routines, either an executable file in the appropriate directory (explained below) named `deploy` (no file extension) or a `Capfile`, which it assumes is from Capistrano.  A custom deploy script will be used whenever its found, and it will fall back to a basic `cap deploy` if a Capfile is found.  If you're using Capistrano but want something more complex than `cap deploy`, write it into a `deploy` script and make sure the file is executable.

### Separate Projects
By default, Scatter will use the basename from the root of the git repository its run from.  For example, let's say you have a git repository in `/Users/evan/code/some-project` and you are currently in a directory like `/Users/evan/code/some-project/sub/directory`.  Running `scatter` here would assume you had a deploy routine in `/path/to/scatter/deploys/some-project`.  If you don't want that, or if you're not using a git repository, or if you just want to run the command from outside your repository, you can pass the deploy directory name as a command line argument.  In this case, let's say your deploy script is in `/path/to/scatter/deploys/other-name`; you would run `scatter other-name`.


## Requirements
Scatter is written in Python, so you'll need it installed.  I think that's about it.  I wrote it to use on OSX, but I suppose there's a chance it works in other environments with Python installed, too.
