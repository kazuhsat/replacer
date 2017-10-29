#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: kazuhsat <kazuhsat555@gmail.com>

import shutil

def file_str_replace(pathname: str, search: str, replace: str, interactive: bool=True) -> bool:
    """file_str_replace(pathname: string, search: string, replace: string, interactive: boolean)

    replace words in a file.
    """
    tmp_pathname = pathname + '.replace'

    with open(pathname, 'r') as search_file, open(tmp_pathname, 'a') as replace_file:
        for line in search_file:
            if search in line:
                if interactive:
                    print('>>> %s' % pathname)
                    print(line, end='')
                    if input("replace with %s ? [y/n] " % search).lower() != 'y':
                        replace_file.write(line)
                        continue;
                replace_file.write(line.replace(search, replace))
            else:
                replace_file.write(line)

    shutil.move(tmp_pathname, pathname)

    return True

if __name__ == "__main__":
    import argparse
    import os.path
    import glob

    parser = argparse.ArgumentParser(prog='replacer', epilog='(END)', add_help=True)

    parser.add_argument('argument', nargs=3)

    parser.add_argument('-f', '--force', action='store_true')
    parser.add_argument('-i', '--interactive', action='store_true')
    parser.add_argument('-r', '-R', '--recursive', action='store_true')

    args = parser.parse_args()

    pathname, search, replace = args.argument

    interactive = False if args.force else True

    if not os.path.exists(pathname):
        print('replacer: %s: No such file or directory' % pathname)

    if os.path.isdir(pathname):
        if args.recursive:
            for (root, dirs, files) in os.walk(pathname):
                for file in files:
                    file_str_replace(os.path.join(root,file), search, replace, interactive)
        else:
            for filename in os.listdir(pathname):
                tmp_pathname = os.path.join(pathname, filename);
                if os.path.isfile(tmp_pathname):
                    file_str_replace(tmp_pathname, search, replace, interactive)
    else:
        file_str_replace(pathname, search, replace, interactive)
