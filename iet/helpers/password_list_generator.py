#!/usr/bin/env python3

import argparse
import rstr
import pyperclip

from iet.core import load_config
from iet.logging import setup_logging


logger = None


def parse_args(print_help=False):
    argparser = argparse.ArgumentParser(prog='genlist')
    argparser.add_argument('-c', '--config', help='Location of config file', default=None)
    argparser.add_argument('-cp', '--copy', help='copy to clipboard', action='store_true')
    argparser.add_argument('-i', '--iters', help='length of wordlist to generate',
                           default='100')
    argparser.add_argument('-o', '--outfile', help='name of the worldlist file',
                           default='iet-wordlist.txt')
    argparser.add_argument('-r', '--regex', help='path to the file or directory to parse',
                           required=True)
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
    regex_list = []
    for i in range(iters):
        regex_list.append(rstr.xeger(regex))
    return regex_list


def write_outfile(outfile, wordlist):
    wordlist = map(lambda x:x+'\n', wordlist)
    with open(outfile, 'w') as f:
        f.writelines(wordlist)


def main(config, iters=100, regex=None, copy=False, stdout=False, write=False, outfile='iet-wordlist.txt'):
    global logger
    logger = setup_logging(load_config(config, 'logging'))
    iters = int(iters.replace('k', '000'))
    if regex:
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
        regex=args.regex,
        copy=args.copy if args.copy else False,
        stdout=args.stdout if args.stdout else False,
        write=args.write if args.write else False,
        outfile=args.outfile if args.outfile else None
    )
