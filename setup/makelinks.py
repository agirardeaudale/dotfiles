#!/usr/bin/env python
""" Andrew Girardeau-Dale
8/22/14

"""

################################## Imports ####################################

import os
import sys
import argparse
try:
    import ipdb as pdb
except ImportError:
    import pdb


################################# Utility ###################################

def englishJoin(stringList):
    """Join a list of strings using commas, spaces, and the word "and", as one
    would in English. Oxford comma is included.

    """

    if len(stringList) >= 2:
        return "{0}, and {1}".format(", ".join(stringList[:-1]), stringList[-1])
    elif len(stringList) == 1:
        return stringList[0];
    else:
        return "[]"


################################# Constants ###################################

files = {
    "vim" :
        [
            {
                "source" : "~/dotfiles/vim/vimrc",
                "link"   : "~/.vimrc"
            },
        ],

    "git" :
        [
            {
                "source" : "~/dotfiles/git/gitconfig",
                "link"   : "~/.gitconfig"
            },
            {
                "source" : "~/dotfiles/git/gitignore",
                "link"   : "~/.gitignore"
            },
        ],

    "bash" :
        [
            {
                "source" : "~/dotfiles/bash/bashrc",
                "link"   : "~/.bashrc"
            },
            {
                "source" : "~/dotfiles/bash/bash_aliases",
                "link"   : "~/.bash_aliases"
            },
            {
                "source" : "~/dotfiles/bash/dircolors",
                "link"   : "~/.dircolors"
            },
        ],

    "python" :
        [
            {
                "source" : "~/dotfiles/python/ipython_config.py",
                "link"   : "~/.ipython/profile_default/ipython_config.py"
            },
        ],

    "tmux" :
        [
            {
                "source" : "~/dotfiles/tmux/tmux.conf",
                "link"   : "~/.tmux.conf"
            },
        ],

    "scripts" :
        [
            {
                "source" : "~/dotflies/scripts/ctagdisplay.py",
                "link"   : "~/bin/ctagdisplay"
            },
        ],

}

potentialGroups = files.keys()
potentialGroupString = englishJoin(['"{0}"'.format(x) for x in potentialGroups])

home = os.path.expanduser("~")

################################# Functions ###################################

def createLinks(fileList):
    for file in fileList:
        source = file["source"].replace("~", home, 1)
        link = file["link"].replace("~", home, 1)
        (linkDirectory, _) = os.path.split(link)
        try:
            os.makedirs(linkDirectory)
        except:
            pass
        if os.path.lexists(link):
            try:
                os.unlink(link)
            except OSError as e:
                print("Couldn't remove existing link at {0}".format(link, str(e)))

        try:
            os.symlink(source, link)
        except OSError as e:
            print("Error linking {0} to {1}: {2}".format(link, source, str(e)))


################################ Control FLow #################################

def getArgumentParser():
    """Construct a command line argument parser.
    
    Returns:
        argParser (argparse.ArgumentParser).
    
    """

    argParser = argparse.ArgumentParser(
            prog="Make links in home directory to dotfiles in repo folder")
    
    helpString = ("Groups of dotfiles to create links for. Options are {0}. "
            "If left blank, all groups will be linked."
            ).format(potentialGroupString)
    argParser.add_argument("groups", nargs="*", metavar="groups",
            help=helpString)
    
    argParser.add_argument("-q", "--quiet", const=True, default=False,
            nargs="?", metavar="quiet mode", dest="quiet",
            help="Suppress program status printing.")

    return argParser

#################################### Main #####################################

def main(argList):

    argParser = getArgumentParser()
    args = argParser.parse_args(argList)

    groups = []
    if not args.groups:
        groups = potentialGroups
    else:
        groups = args.groups
        for group in groups:
            if group not in potentialGroups:
                raise ValueError('Group "{0}" not recognized. Options are {1}.'
                        .format(group, potentialGroupString))
    
    for group in groups:
        createLinks(files[group])

if __name__ == "__main__":
    main(sys.argv[1:])
