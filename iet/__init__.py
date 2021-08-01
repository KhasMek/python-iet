#!/usr/bin/env/python3

from . import bootstrap
from iet.core import find_config
from iet.helpers import ip_calc
from iet.helpers import wordlist_generator


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

def iet_wordlist_generator():
    args = wordlist_generator.parse_args()
    config = find_config(args)
    wordlist_generator.main(
        config,
        iters=args.iters if args.iters else None,
        basic=args.basic if args.basic else False,
        regex=args.regex if args.regex else None,
        copy=args.copy if args.copy else False,
        stdout=args.stdout if args.stdout else False,
        write=args.write if args.write else False,
        outfile=args.outfile if args.outfile else None
    )
