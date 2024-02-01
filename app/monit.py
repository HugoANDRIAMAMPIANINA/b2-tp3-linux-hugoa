#!/usr/bin/env python
from argparse import ArgumentParser
import sys
from arguments import argument_management
from core_functions import system_check, list_checks, get_last_check, get_average_check_values
from file_handler import create_file, file_exists


def main():
    parser = ArgumentParser()
    args = argument_management(parser)

    if not file_exists("/etc/monit/monit.conf"):
        create_file("/etc/monit/", "monit.conf", {"tcp_ports": []})

    if args.check is True:
        system_check()
    if args.list is True:
        list_checks()
    if args.get_last is True:
        get_last_check()
    if args.get_avg is not None:
        get_average_check_values(args.get_avg)

    if (
        args.check is False
        and args.list is False
        and args.get_last is False
        and args.get_avg is None
    ):
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    sys.path.append("/usr/share/monit/")
    main()
