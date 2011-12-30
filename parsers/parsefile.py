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
import re
import javaparser
import pythonparser
import xmlparser


java_pattern = re.compile('\.java$')
php_pattern = re.compile('\.php$')
xml_pattern = re.compile('\.xml$')
python_pattern = re.compile('\.py$')


def _parse_file(arg, cmd_options):
    if cmd_options['verbose']:
        print "Parsing file %(file)s..." % {'file': arg}

    if java_pattern.search(arg) != None:
        javaparser.parse(arg, cmd_options)
    elif xml_pattern.search(arg) != None:
        xmlparser.parse(arg, cmd_options)
    elif python_pattern.search(arg) != None:
        pythonparser.parse(arg, cmd_options)


def parse(arg, cmd_options):
    '''
    Check the file extension, and call the right parser
    '''
    _parse_file(arg, cmd_options)
