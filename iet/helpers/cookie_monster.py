#!/usr/bin/env python3

import argparse
import requests
import urllib3

from iet.core import load_config
from iet.logging import setup_logging


logger = None


def parse_args(print_help=False):
    argparser = argparse.ArgumentParser(prog='cookie_monster')
    argparser.add_argument('-c', '--config', help='Location of config file', default=None)
    argparser.add_argument('-nv', '--no-verify', help='Disable Certificate verification',
                           action='store_true',
                           default=False)
    argparser.add_argument('-o', '--outfile', help='Write cookies to file')
    argparser.add_argument('target', help='Target domain to get cookies of')
    args = argparser.parse_args()
    if print_help:
        return argparser.print_help()
    else:
        return args


def write_outfile(outfile, cookies):
    cookies = map(lambda x:x+'\n', cookies)
    with open(outfile, 'w') as f:
        f.writelines(cookies)


def main(config, target=None, outfile=None, no_verify=False):
    global logger
    logger = setup_logging(load_config(config, 'logging'))
    session = requests.Session()
    if no_verify:
        logger.debug("Disable SSL Verificaiton: %s" % no_verify)
        urllib3.disable_warnings()
        session.get(target, verify=False)
    else:
        try:
            session.get(target)
        except Exception as e:
            logger.error(e)
            logger.error("Have you tried with -nv?")
    cookies = session.cookies.get_dict()
    if cookies:
        for k,v in cookies.items():
            logger.info("%s: %s" % (k, v))
    else:
        logger.info("%s does not assign any cookies" % target)
    if outfile:
        write_outfile(outfile, cookies)    


if __name__ == "__main__":
    args = parse_args()
    main(
        args.config,
        target=args.target,
        outfile=args.outfile if args.outfile else None,
        no_verify=args.no_verify if args.no_verify else False
    )
