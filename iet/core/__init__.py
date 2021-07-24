import os
import pkg_resources
import yaml

from pathlib import Path


def find_config(args):
    config = ''
    if args.config:
        config = args.config
    elif os.path.isfile(os.path.join(Path.home(), '.iet', 'config.yaml')):
        config = os.path.join(Path.home(), '.iet', 'config.yaml')
    else:
        config = pkg_resources.resource_filename(__name__, "../config.yaml")
    return config


def load_config(config, section=None):
    config = open(config, 'r')
    config = yaml.load(config, Loader=yaml.FullLoader)
    if section:
        config = config[section]
    return config
