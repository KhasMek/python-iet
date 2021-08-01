#!/usr/bin/env python3

import argparse
import datetime
import pyperclip
import rstr
import sys

from iet.core import load_config
from iet.logging import setup_logging


logger = None


def parse_args(print_help=False):
    argparser = argparse.ArgumentParser(prog='genlist')
    argparser.add_argument('-b', '--basic', help='generate basic (seasonal) wordlist',
                           action='store_true')
    argparser.add_argument('-c', '--config', help='location of config file', default=None)
    argparser.add_argument('-cp', '--copy', help='copy to clipboard', action='store_true')
    argparser.add_argument('-i', '--iters', help='length of wordlist to generate',
                           default='100')
    argparser.add_argument('-o', '--outfile', help='name of the worldlist file',
                           default='iet-wordlist.txt')
    argparser.add_argument('-r', '--regex', help='path to the file or directory to parse')
    argparser.add_argument('-s', '--stdout', help='print list to terminal',
                           action='store_true')
    argparser.add_argument('-w', '--write', help='write the wordlist to file',
                           action='store_true')
    args = argparser.parse_args()
    if print_help:
        return argparser.print_help()
    else:
        return args


def gen_regex_list(regex, iters):
    regex_list = set()
    for i in range(iters):
        regex_list.add(rstr.xeger(regex))
    return regex_list


def gen_seasonal_wordlist(month_spread=5, seasons=None, end_characters='!.'):
    seasonal_list = set()
    today = datetime.datetime.now()
    current_month = int(today.strftime("%m").lstrip('0'))
    current_year = int(today.strftime("%Y"))
    season = [season for season, months in seasons.items() if current_month in months][0]
    for char in end_characters:
        seasonal_list.add("%s%s%s" % (season, current_year, char))
        seasonal_list.add("%s%s%s" % (season.capitalize(), current_year, char))
        for x in range(0, month_spread):
            mod_month = current_month - x
            if mod_month <= 0:
                mod_month = mod_month + 12
            _month = datetime.date(current_year, mod_month, int(today.strftime("%d"))).strftime("%B")
            seasonal_list.add("%s%s%s" % (_month, current_year, char))
            seasonal_list.add("%s%s%s" % (_month.lower(), current_year, char))
    return seasonal_list


def write_outfile(outfile, wordlist):
    wordlist = map(lambda x:x+'\n', wordlist)
    with open(outfile, 'w') as f:
        f.writelines(wordlist)


def main(config, iters=100, basic=False, regex=None, copy=False, stdout=False, write=False, outfile='iet-wordlist.txt'):
    global logger
    logger = setup_logging(load_config(config, 'logging'))
    config = load_config(config, 'wordlists')
    iters = int(iters.replace('k', '000'))
    wordlist = ''
    if (not basic) and (not regex):
        logger.error("You must provide regex or generate a basic list!")
        sys.exit(0)
    if basic:
        logger.debug("Generating basic seasonal wordlist")
        wordlist = gen_seasonal_wordlist(config['month_spread'], config['seasons'], config['end_characters'])
    if regex:
        logger.debug("Generating wordlist based off regular expression (%s)" % regex)
        if wordlist:
            regex_wordlist = gen_regex_list(regex, iters)
            wordlist.update(regex_wordlist)
        else:
            wordlist = gen_regex_list(regex, iters)
    if stdout:
        for line in wordlist:
            logger.info(line)
    if write:
        write_outfile(outfile, wordlist)
        logger.info("Wordlist written to %s" % outfile)
    if copy:
        try:
            pyperclip.copy('\n'.join(wordlist))
            logger.info("Wordlist copied to the clipboard")
        except pyperclip.PyperclipException:
            logger.error("Could not find a copy/paste mechanism for your system.")


if __name__ == "__main__":
    args = parse_args()
    main(
        args.config,
        iters=args.iters if args.iters else None,
        basic=args.basic if args.basic else False,
        regex=args.regex if args.regex else None,
        copy=args.copy if args.copy else False,
        stdout=args.stdout if args.stdout else False,
        write=args.write if args.write else False,
        outfile=args.outfile if args.outfile else None
    )
