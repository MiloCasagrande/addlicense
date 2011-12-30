#!/usr/bin/python
# -*- coding: UTF-8 -*-
#==============================================================================
# Copyright (C) 2011  Milo Casagrande <milo@ubuntu.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#==============================================================================
import os
from optparse import OptionParser
import time
import crawldirs


__author__ = "Milo Casagrande"
__copyright__ = "Copyright 2011, Milo Casagrande"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "milo@ubuntu.com"


included_files = []
excluded_dirs = []

cmd_options = {'year': '', 'holder': '', 'holder_email': '', 'license': '', \
               'verbose': False}
valid_licenses = ['apache2', 'gpl3']


def _check_options(options):
    if (options.license == None) or (options.license not in valid_licenses):
        print "\nErr: must provide a valid license: none provided or not valid.\n"
        exit(2)
    else:
        cmd_options['license'] = options.license

    if options.year == None:
        cmd_options['year'] = time.strftime("%Y")
    else:
        cmd_options['year'] = options.year

    if options.holder_email != None:
        cmd_options['holder_email'] = options.holder_email

    if options.holder == None:
        # guess something that can recall a user name
        cmd_options['holder'] = os.getlogin()
    else:
        cmd_options['holder'] = options.holder

    cmd_options['verbose'] = options.verbose

    if options.exclude != None:
        for exclude in options.exclude:
            excluded_dirs.append(os.path.basename(exclude))

    if options.file != None:
        for include in options.file:
            included_files.append(include)


def _check_args(args):
    for arg in args:
        if (not os.path.isdir(arg)) or (not os.path.exists(arg)):
            print "Err: Argument must be a valid directory: %(arg)s" \
            % {'arg': arg}
            exit(2)


def main():
    usage = "%prog DIR1 DIR2 ... -l LICENSE [OPTIONS]"
    parser = OptionParser(usage)
    parser.prog = "addlicense"
    parser.version = "0.1"
    parser.description = "Add license header to all the files in the \
specified directories (and their sub-directories). If no directory is \
specified, the current working directory will be considered. \
Insert license headers for Java and PHP files, based on the file \
extension. Supported licenses are: Apache v2, GPL v3"

    parser.add_option("-e", "--exclude", dest="exclude", \
                      help="exclude all files in DIR and sub-DIRs", \
                      metavar="DIR", action="append")
    parser.add_option("-f", "--file", dest="file", help="include FILE, has to be an absolute path",
                      metavar="FILE", action="append")
    parser.add_option("-l", "--license", dest="license", \
                      help="add LICENSE header; accepted LICENSEs are: \
                      'apache2', 'gpl3'", \
                      action="store", metavar="LICENSE")
    parser.add_option("-y", "--year", metavar="YEAR", dest="year", \
                      help="use YEAR as the license year; default \
                      is the current year", \
                      action="store")
    parser.add_option("-r", "--holder", metavar="HOLDER", dest="holder", \
                      action="store", \
                      help="use HOLDER as the copyright's holder")
    parser.add_option("-m", "--email", metavar="EMAIL", dest="holder_email", \
                      action="store", \
                      help="use EMAIL as the email of the copyright's holder")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", \
                      help="be verbose", default=False)

    (options, args) = parser.parse_args()

    if len(args) == 0 and (options.license == None or options.license not in valid_licenses):
        print "Usage: addlicense DIR1 DIR2 ... -l LICENSE [OPTIONS]\n"
        print "Type 'addlicense -h' for more information."
        exit(2)

    # if no directory is specified, add the current one
    if len(args) == 0 and options.file == None:
        args.append(os.getcwd())

    if len(args) > 0:
        _check_args(args)

    _check_options(options)

    crawldirs.crawl(args, cmd_options, excluded_dirs, included_files)


if __name__ == '__main__':
    main()
    exit(0)
