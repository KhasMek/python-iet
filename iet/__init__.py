#!/usr/bin/env/python3

from . import bootstrap
from iet.core import find_config
from iet.helpers import ip_calc


def iet_bootstrap():
    args = bootstrap.parse_args()
    config = find_config(args)
    bootstrap.main(config, args.basename, args.project_name, args.project_type)


def iet_ip_calc():
    args = ip_calc.parse_args()
    config = find_config(args)
    ip_calc.main(
                config,
                _type=args.type if args.type else None,
                target=args.target,
                netblock=args.netblock if args.netblock else None
                )
