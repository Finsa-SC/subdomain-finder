from validate import check_subdomain

from dotenv import load_dotenv
import os
import argparse


### Init env
load_dotenv()
TIMEOUT = float(os.getenv("TIMEOUT", 3.0))
THREAD = int(os.getenv("THREAD", 10))
DEBUG = os.getenv("DEBUG", "false").lower().strip() == "true"

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
        "-o",
        "--output",
        help="Save recon result"
    )

    args = parser.parse_args()

    if args.redirect and not args.verbose:
        parser.error("redirect need verbose to show")

    if args.domain:
        check_subdomain(
            args.domain,
            args.timeout,
            args.thread,
            args.available,
            args.verbose,
            args.redirect
        )
    elif args.domain_list:
        check_subdomain(
            args.domain_list,
            args.timeout,
            args.thread,
            args.available,
            args.verbose,
            args.redirect
        )

if __name__ == "__main__":
   main()