#!/usr/bin/env python

# The purpose of this script is to open a GnuCash data-base and save
# it under another name.

import argparse
from urllib.parse import urlparse
import gnucash
from gnucash import (
    Session, GnuCashBackendException,
    SessionOpenMode,
    ERR_BACKEND_LOCKED,
    ERR_FILEIO_FILE_NOT_FOUND,
    gnucash_core_c,
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
parser.add_argument(
    '--progress',
    action='store_true',
    help='Generate progress output.',
)

args = parser.parse_args()

inputParts = urlparse(args.input)
outputParts = urlparse(args.output)

print(inputParts)
print(outputParts)

if args.progress:
    percentageFunc = gnucash_core_c.qof_percentage_func(lambda a, b: print(a, b) if a else print(b))
else:
    percentageFunc = None

try:
    inputSession = gnucash_core_c.qof_session_new(gnucash_core_c.qof_book_new())
    gnucash_core_c.qof_session_begin(inputSession, args.input, SessionOpenMode.SESSION_READ_ONLY)
    gnucash_core_c.qof_session_load(inputSession, percentageFunc)
except GnuCashBackendException as backend_exception:
    print(backend_exception)
    exit

try:
    outputSession = gnucash_core_c.qof_session_new(gnucash_core_c.qof_book_new())
    gnucash_core_c.qof_session_begin(outputSession, args.output, SessionOpenMode.SESSION_NEW_OVERWRITE)
#    gnucash_core_c.qof_session_save(outputSession, None)
except GnuCashBackendException as backend_exception:
    print(backend_exception)
    exit

gnucash_core_c.qof_session_swap_data(inputSession, outputSession)
gnucash_core_c.qof_book_mark_session_dirty(gnucash_core_c.qof_session_get_book(outputSession))

gnucash_core_c.qof_session_save(outputSession, percentageFunc)
gnucash_core_c.qof_session_end(outputSession)
