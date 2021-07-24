#!/usr/bin/env/python3

from . import bootstrap
from iet.core import find_config


def iet_bootstrap():
    args = bootstrap.parse_args()
    config = find_config(args)
    bootstrap.main(config, args.basename, args.project_name, args.project_type)
