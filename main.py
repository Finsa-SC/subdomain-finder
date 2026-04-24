from concurrent.futures import thread

from validate import check_subdomain
from save_file import save_file_healthy, save_file_problem
from scan_config import ScanConfig

from dotenv import load_dotenv
import os
import argparse


### Init env
load_dotenv()
TIMEOUT = float(os.getenv("TIMEOUT", 3.0))
THREAD = int(os.getenv("THREAD", 10))
DEBUG = os.getenv("DEBUG", "false").lower().strip() == "true"
DELAY = os.getenv("DELAY", 0.0)

VERSION = "1.0.0"

def main():
    parser = argparse.ArgumentParser(description="Subdomain recon tool")

    group = parser.add_mutually_exclusive_group(required=True)

##Version
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"subf {VERSION}",
        help="Print version of the tool"
    )


##Input
    group.add_argument(
        "-d",
        "--domain",
        help="Search for single domain"
    )

    group.add_argument(
        "-dL",
        "--domain-list",
        help="Validate multiple domain from file"
    )

    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=TIMEOUT,
        help="Request timeout (default is 3 sec)"
    )

    parser.add_argument(
        "-th",
        "--thread",
        type=int,
        default=THREAD,
        help="Number of threads (default is 10)"
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=DELAY,
        help="Delay of request"
    )

##Inputless
    parser.add_argument(
        "-A",
        "--available",
        action="store_true",
        help="Only show domain with 200 status code"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show information more detail"
    )

    parser.add_argument(
        "-r",
        "--redirect",
        action="store_true",
        help="Show redirect information"
    )

    parser.add_argument(
        "-nW",
        "--no-wildcard",
        action="store_true",
        help="Skip subdomain if wildcard dns detected in that's subdomain"
    )

    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Show clean output in terminal only subdoamin with http/https 200 status code"
    )

    parser.add_argument(
        "--ip",
        action="store_true",
        help="Show ip address instead subdomain clearly"
    )

    parser.add_argument(
        "-T",
        "--title",
        action="store_true",
        help="Print title of page below subdomain"
    )

    parser.add_argument(
        "-x",
        "--header-tech",
        action="store_true",
        help="Show subdomain tech from header"
    )

    parser.add_argument(
        "-o",
        "--output",
        action="store_true",
        help="Save recon result as plain list ip"
    )

    parser.add_argument(
        "-oJ",
        "--output-json",
        action="store_true",
        help="Save recon result as json with detail information"
    )

    args = parser.parse_args()

    config = ScanConfig(
        timeout=args.timeout,
        thread=args.thread,
        available=args.available,
        verbose=args.verbose,
        redirect=args.redirect,
        no_wildcard=args.no_wildcard,
        quiet=args.quiet,
        quiet_ip=args.ip,
        show_title=args.title,
        show_tech=args.header_tech,
        save_file_plain=args.output,
        save_file_json=args.output_json,
        delay=args.delay
    )

    if args.redirect and not args.verbose:
        parser.error("redirect need verbose to show")
    if args.ip and not args.quiet:
        parser.error("Ip need quiet to show")

    if args.domain:
        check_subdomain(args.domain, config)
    elif args.domain_list:
        check_subdomain(args.domain_list, config)

if __name__ == "__main__":
   main()