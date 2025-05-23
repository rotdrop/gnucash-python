#!/usr/bin/env python

# The purpose of this script is to open a GnuCash data-base and save
# it under another name.

import argparse
from urllib.parse import urlparse
from gnucash import (
    Session, GnuCashBackendException,
    SessionOpenMode,
    ERR_BACKEND_LOCKED, ERR_FILEIO_FILE_NOT_FOUND
)

parser = argparse.ArgumentParser(
    description='set order and stabilization'
)
parser.add_argument(
    'input',
    help='Input URI, e.g. "xml://foobar.xml".',
)
parser.add_argument(
    'output',
    help='Output URI, e.g. mysql://user:password@host/database".',
)

args = parser.parse_args()

inputParts = urlparse(args.input)
outputParts = urlparse(args.output)

print(inputParts)
print(outputParts)

try:
    inputSession = Session(args.input)
except GnuCashBackendException as backend_exception:
    print(backend_exception)
    exit

try:
    outputSession = Session(args.output, SessionOpenMode.SESSION_NEW_OVERWRITE)
except GnuCashBackendException as backend_exception:
    print(backend_exception)
    exit
