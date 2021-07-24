#!/usr/bin/python3

"""
TODO: I should start using ipaddress and drop the reqirement for ipcalc if possible
TODO: support formats like 192.0.2.8[0-5]
"""

import argparse
import ipcalc

from colorama import Fore
from iet.core import load_config
from iet.logging import setup_logging
from texttable import Texttable


logger = None

table = Texttable()
table2 = Texttable()


def parse_args(print_help=False):
    argparser = argparse.ArgumentParser(prog='ip_calc')
    argparser.add_argument('-c', '--config', help='Location of config file', default=None)
    argparser.add_argument('type', help='Type of query to perform. \
                           (default: %(default)s)', default='summary',
                           choices=['summary', 'range', 'isitin'])
    argparser.add_argument('target', help='Target ip address, range or subnet')
    argparser.add_argument('-n', '--netblock', help='Netblock to look up for ' +
                           'isitin function')
    args = argparser.parse_args()
    if print_help:
        return argparser.print_help()
    else:
        return args


def summary(subnet):
    for query in subnet:
        table.set_chars(['', '', '', ''])
        table.set_cols_width([2, 15, 20])
        table.set_deco(Texttable.BORDER)
        table.add_row(["", "Query:", query])
        query = ipcalc.Network(query)
        table.add_row(["", "Subnet ID:", str(query.network())])
        table.add_row(["", "Broadcast:", str(query.broadcast())])
        table.add_row(["", "Netmask:", str(query.netmask())])
        # TODO: Fix when it's a single IP
        table.add_row(["", "Usable IP's:", str(query.size() - 2)])
        table.add_row(["", "IP Version:", str(query.version())])
        table.add_row(["", "Information:", str(query.info())])
        logger.info(table.draw())
        table.reset()


def range(subnet):
    for query in subnet:
        summary([query])
        table2.set_chars(['', '', '', ''])
        table2.set_cols_align(["", "c", "c"])
        table2.set_cols_valign(["", "m", "m"])
        table2.set_cols_width([2, 15, 15])
        table2.header(['', 'Subnet', 'Address'])
        ips = ""
        for ip in ipcalc.Network(query):
            ips += str(ip) + "\n"
        row = '', query, ips
        table2.add_row(row)
        logger.info(table2.draw())
        table2.reset()


def isitin(net, key):
    result = ipcalc.Network(net).has_key(key)
    if result == True:
        logger.info("True: " + key + " is in the " + net + " Subnet!")
    else:
        logger.info(Fore.RED + "FALSE: " + key + " is not in the " + net + " Subnet!")


def main(config, _type=None, target=None, netblock=None):
    global logger
    logger = setup_logging(load_config(config, 'logging'))
    if _type == 'summary':
        summary([target])
    if _type == "range":
        range([target])
    if _type == "isitin":
        key = target
        net = netblock
        isitin(net, key)


if __name__ == "__main__":
    args = parse_args()
    main(
        args.config, 
        _type=args.type if args.type else None, 
        target=args.target, 
        netblock=args.netblock if args.netblock else None
        )
