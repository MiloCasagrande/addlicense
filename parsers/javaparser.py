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
import shutil
import tempfile
from licenses import javalicenses

java_license_pattern = re.compile("^\/\*\s*\*\s*[Copyright]\s*")


def parse(arg, cmd_options):
    tmp_file = tempfile.NamedTemporaryFile('a', delete=False)
    with open(arg, 'r') as read_file:
        # check if we already have the license header
        license_lines = ""
        for i in range(4):
            license_lines += read_file.readline()

        if java_license_pattern.match(license_lines):
            return
        else:
            read_file.seek(-read_file.tell(), os.SEEK_CUR)

        old = read_file.read()

    with open(tmp_file.name, 'a') as write_file:
        write_file.write(javalicenses.get_license_string(cmd_options['license']) \
                         % cmd_options)
        write_file.write(old)
        write_file.flush()

    shutil.move(tmp_file.name, arg)
