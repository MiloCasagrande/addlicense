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
import re
from parsers import parsefile

hidden_files_pattern = re.compile("^\.\w+")


def _crawl_dir(args, cmd_options, excluded_dirs, cwd=None):
    '''
    Traverse the directories and perform some checks on dir and file names
    '''
    for arg in args:
        if len(excluded_dirs) > 0 and os.path.basename(arg) in excluded_dirs:
            continue

        if hidden_files_pattern.match(os.path.basename(arg)) != None:
            continue

        if cwd != None:
            arg = os.path.join(cwd, arg)

        if os.path.exists(arg):
            if os.path.isfile(arg):
                parsefile.parse(arg, cmd_options)
            elif os.path.isdir(arg):
                _crawl_dir(os.listdir(arg), cmd_options, excluded_dirs, arg)
        else:
            print "File or directory '%(arg)s' does not exist. It will not be considered." % {'arg': arg}


def _recurse_file(included_files, cmd_options):
    '''
    Parse the file passed in 'included_files', and add the license
    '''
    for f in included_files:
        if os.path.exists(f) and os.path.isfile(f):
            parsefile.parse(f, cmd_options)
        else:
            print "File or directory '%(arg)s' does not exist. It will not be considered." % {'arg': f}


def crawl(args, cmd_options, excluded_dirs, included_files):
    '''
    Traverse the directories in 'args', and add the license to the files in
    them.
    '''
    _crawl_dir(args, cmd_options, excluded_dirs)

    if len(included_files) > 0:
        _recurse_file(included_files, cmd_options)
