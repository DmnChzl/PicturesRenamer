# -*- coding: utf-8 -*-
'''
Copyright (C) 2016 Damien Chazoule

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import re
import sys
import time

from PIL import Image
from datetime import datetime

LOG = False
FORCE = False
PREFIX = "IMG_"
TEMPLATE = "%Y%m%d_%H%M%S"

def extract_time(file):
    if not os.path.isfile(file):
        return None

    info = time.gmtime(os.path.getmtime(file))
    try:
        img = Image.open(file)
        if hasattr(img, "_getexif"):
            exifdata = img._getexif()
            exif = exifdata[0x9003]
            exif = datetime.strptime(exif, "%Y:%m:%d %H:%M:%S")
            return exif.strftime(TEMPLATE)
    except:
        print('Error : Exif data not existing')

    return time.strftime(TEMPLATE, info)

def format_time(file):
    datetime = extract_time(file)
    if datetime is None:
        return None

    datetime = re.sub("[^A-Za-z0-9_,. ]", "_", datetime)
    return str(datetime)

def rename_file(file):
    if not os.path.isfile(file):
        return 0

    ext = os.path.splitext(file)[1]
    if ext.lower() not in [".jpg", ".jpeg", ".png"]:
        return 0

    path, base = os.path.split(file)
    datetime = format_time(file)
    if datetime is None:
        return 0

    if not FORCE:
        if base.startswith(PREFIX):
            return 0

    new_filename = PREFIX + datetime + ext
    path_filename = os.path.join(path, new_filename)

    try:
        os.rename(file, path_filename)
        if LOG:
            with open("log.txt", "a") as text:
                text.write("Success : '{}' renamed to '{}' ;\n".format(base, new_filename))
        return 1
    except:
        if LOG:
            with open("log.txt", "a") as text:
                text.write("Error : Can\'t rename '{}' to '{}' ;\n".format(base, new_filename))
        return 0

def rename_files_in_directory(directory):
    files = os.listdir(directory)
    count = 0
    for i in files:
        file = os.path.join(directory, i)
        count += rename_file(file)

    return count

def identify_arg(arg):
    global LOG
    global FORCE
    global PREFIX
    global TEMPLATE

    values = arg.split("=")
    if len(values) == 1:
        if values[0] in ["-l", "--log"]:
            LOG = True
        elif values[0] in ["-f", "--force"]:
            FORCE = True
        else:
            print("Unknown option : '{}'".format(values[0]))
            sys.exit(1)
    elif len(values) == 2:
        if values[0] in ["-p", "--prefix"]:
            PREFIX = values[1]
        elif values[0] in ["-t", "--template"]:
            TEMPLATE = values[1]
        else:
            print("Unknown option : '{}'".format(values[0]))
            sys.exit(1)
    else:
        print("Unknown option : '{}'".format(values[0]))
        sys.exit(1)

def use_assistant():
    global LOG
    global FORCE
    global PREFIX
    global TEMPLATE

    one = input("Would you specify the prefix (y/N) ? ")
    if one.lower() in ["y", "yes"]:
        PREFIX = input("Specify the prefix : ")

    two = input("Would you specify the template (y/N) ? ")
    if two.lower() in ["y", "yes"]:
        TEMPLATE = input("Specify the template : ")

    three = input("Would you display logs (y/N) ? ")
    if three.lower() in ["y", "yes"]:
        LOG = True

    four = input("Would you force process (y/N) ? ")
    if four.lower() in ["y", "yes"]:
        FORCE = True

def show_help():
    print('''Usage : pictures_renamer.py [directory | file.[jpeg|jpg|png]] [option] ...
Options available :
-a : use the assistant (also --ask)
-f : force the process (also --force)
-h : print this help message (also --help)
-l : create .txt with logs of the process (also --log)
-p : modify default value of the prefix, use it like this : '-p=[value]' (also --prefix)
-t : modify default value of the template of date, use it like this : '-t=[value]' (also --template)
''')

if __name__ == "__main__":
    args = list(sys.argv)
    args.remove("pictures_renamer.py")
    if len(args) > 0:
        if "-h" in args:
            show_help()
            sys.exit(1)
        elif "--help" in args:
            show_help()
            sys.exit(1)
        elif "-a" in args:
            path = args[0]
            use_assistant()
        elif "--ask" in args:
            path = args[0]
            use_assistant()
        else:
            path = args[0]
            for x in range(1, len(args)):
                identify_arg(args[x])
    else:
        print('''Usage : pictures_renamer.py [directory | file.[jpeg|jpg|png]]''')
        sys.exit(1)

    if os.path.isfile(path):
        rename_file(path)
    elif os.path.isdir(path):
        count = rename_files_in_directory(path)
        print("{} file(s) renamed".format(count))
        if LOG:
            with open("log.txt", "a") as log:
                log.write("\n{} file(s) renamed.\n".format(count))
    else:
        print("Error : Path {} not found".format(path))
