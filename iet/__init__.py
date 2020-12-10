#!/usr/bin/env/python3

import argparse
import os
import pkg_resources

from . import bootstrap
from pathlib import Path


def iet():
    args = bootstrap.parse_args()
    if args.config:
        config = args.config
    elif os.path.isfile(os.path.join(Path.home(), '.iet', 'config.yaml')):
        config = os.path.join(Path.home(), '.iet', 'config.yaml')
    else:
        config = pkg_resources.resource_filename(__name__, "config.yaml")
    bootstrap.main(config, args.basename, args.project_name)
