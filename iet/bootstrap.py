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
    argparser.add_argument('-pn', '--project_name', help='project directory name', default=None)
    args = argparser.parse_args()
    if print_help:
        return argparser.print_help()
    else:
        return args


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


def main(config, basename, project_name):
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
    config = load_config(config, 'bootstrap')
    logger.info("basename: %s" % basename,)
    logger.info("project name: %s" % project_name)
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
            # TODO: this could be a cleaner check
            try:
                copyfile(copy_file, dst)
                logger.debug("Copied %s to %s" % (copy_file, dst))
            except FileNotFoundError:
                if os.path.isfile(os.path.join(Path.home(), '.iet', copy_file)):
                    copy_file = os.path.join(Path.home(), '.iet', copy_file)
                    copyfile(copy_file, dst)
                    logger.debug("Copied %s to %s" % (copy_file, dst))
                elif pkg_resources.resource_filename(__name__, copy_file):
                    copy_file = pkg_resources.resource_filename(__name__, copy_file)
                    copyfile(copy_file, dst)
                    logger.debug("Copied %s to %s" % (copy_file, dst))
    # I don't know if this should go before or after the file/folder creation
    # maybe get the vars first, then open/write the .in/.out file instead of moving and sed'ing
    mkvars(config['vars'])


if __name__ == "__main__":
    args = parse_args()
    main(args.config, args.basename, args.project_name)
