#!/usr/bin/env python3

import argparse
import os
import pkg_resources
import yaml

from colorama import Fore, Style
from iet.logging import setup_logging
from pathlib import Path
from pprint import pprint
from shutil import copyfile


logger = None


def parse_args(print_help=False):
    argparser = argparse.ArgumentParser(prog='bootstrap')
    argparser.add_argument('-c', '--config', help='Location of config file', default=None)
    argparser.add_argument('-b', '--basename', help='directory to bootstrap', default=os.getcwd())
    argparser.add_argument('-pt', '--project_type', help='project directory name', default='default')
    argparser.add_argument('-pn', '--project_name', help='project directory name', default=None)
    args = argparser.parse_args()
    if print_help:
        return argparser.print_help()
    else:
        return args

# I should refactor this to another module cause imma use it more than here
def load_config(config, section=None):
    config = open(config, 'r')
    config = yaml.load(config)
    if section:
        config = config[section]
    return config


def mkvars(vars):
    """
    build a dictionary and return it?
    """
    iet_vars = {}
    logger.debug("vars: %s" % vars)
    for var in vars:
        iet_vars[var] = text = input(Fore.MAGENTA + " [+] Please enter value for %s: " % var + Style.RESET_ALL)
    return iet_vars


def get_file_path(copy_file):
    """
    Find the first instance of the specified file and return the path.
    """
    if os.path.isfile(copy_file):
        pass
    elif os.path.isfile(os.path.join(Path.home(), '.iet', copy_file)):
        copy_file = os.path.join(Path.home(), '.iet', copy_file)
    elif pkg_resources.resource_filename(__name__, copy_file):
        copy_file = pkg_resources.resource_filename(__name__, copy_file)
    return copy_file


def do_copy_update_file(copy_file, dst, iet_vars):
    """
    For the copy file, check iet_vars and replace the variables if
    present in the copy file.
    """
    with open(copy_file, 'r') as copy_data:
        copy_data = copy_data.read()
    for k, v in iet_vars.items():
        var = str("${%s}" % k.upper())
        logger.debug("Searching for: %s" % var)
        if var in copy_data:
            logger.debug("Found %s in %s" % (var, copy_file))
            copy_data = copy_data.replace(var, v)
    with open(dst, 'w') as outfile:
        logger.debug("Writing %s" % dst)
        outfile.write(copy_data)
    return True


def main(config, basename, project_name, project_type):
    """
    - load config file
    - create base directory and subdirs from config.
       - we use makedirs over makedir in case the parent
       directory needs to be created too
    - move .in and .out (and other files??) over
    - set vars for ssh ports,etc. This stage needs more work atm
    """
    global logger
    logger = setup_logging(load_config(config, 'logging'))
    config = load_config(config, 'bootstrap')[project_type]
    logger.info("project type: %s" % project_type)
    logger.info("basename: %s" % basename,)
    logger.info("project name: %s" % project_name)
    iet_vars = mkvars(config['vars'])
    logger.debug("iet variables: %s" % iet_vars)
    for _dir in config['dirs']:
        logger.debug("Creating directory: %s" % _dir)
        os.makedirs(os.path.join(basename, project_name, _dir))
    for file_dirs in config['files']:
        logger.debug("Files copy dir: %s - %s" % (file_dirs, ', '.join(config['files'][file_dirs])))
        for copy_file in config['files'][file_dirs]:
            src = os.path.basename(copy_file)
            if file_dirs in 'basedir':
                dst = os.path.join(basename, project_name, src)
            else:
                dst = os.path.join(basename, project_name, file_dirs, src)
            do_replace = True
            if copy_file.endswith('-noreplace'):
                do_replace = False
                copy_file = copy_file.replace('-noreplace', '')
            copy_file = get_file_path(copy_file)
            if do_replace:
                if do_copy_update_file(copy_file, dst, iet_vars):
                    logger.debug("Copied %s to %s" % (copy_file, dst))
                else:
                    logger.error("ERROR: could not copy %s to %s" % (copy_file, dst))
            else:
                logger.debug("Not performing find/replace on %s" % copy_file)
                copyfile(copy_file, dst)
                logger.debug("Copied %s to %s" % (copy_file, dst))


if __name__ == "__main__":
    args = parse_args()
    main(args.config, args.basename, args.project_name, args.project_type)
