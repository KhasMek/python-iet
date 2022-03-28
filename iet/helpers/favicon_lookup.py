#!/usr/bin/env python3

"""
Full credit to this code goes to phor3nsic
https://github.com/phor3nsic/favicon_hash_shodan
"""

import argparse
import codecs
import mmh3
import requests

from iet.core import load_config
from iet.logging import setup_logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = None

def parse_args(print_help=False):
    argparser = argparse.ArgumentParser(prog='favicon_lookup')
    argparser.add_argument('-c', '--config', help='Location of config file', default=None)
    argparser.add_argument('target', help='Target faviocon URL')
    args = argparser.parse_args()
    if print_help:
        return argparser.print_help()
    else:
        return args

def main(config, target):
    global logger
    shodan_base_url = "https://www.shodan.io/search?query=http.favicon.hash%3A"
    logger = setup_logging(load_config(config, 'logging'))
    response = requests.get(target, verify=False)
    logger.debug("Response: %s" % response)
    favicon = codecs.encode(response.content,"base64")
    favicon_hash = mmh3.hash(favicon)

    logger.debug("Favicon hash: %s" % favicon_hash)
    shodan_hash_url = "%s%s" % (shodan_base_url, favicon_hash)
    logger.info("Results: %s" % shodan_hash_url)

if __name__ == "__main__":
    args = parse_args()
    main(
        args.config,
        target=args.target
        )
