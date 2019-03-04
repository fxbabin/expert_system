
##################
#   Librairies   #
##################

from pathlib import Path
import argparse
import sys
import errno
import os
import re

#############
#   Class   #
#############


class Setting:

    def __init__(self):
        self.file = ""
        self.instructions = []
        self.get_arguments(sys.argv[1:])
        self.check_file()

    def get_arguments(self, args=None):
        """
        Check the input arguments of the program
            :param args=None: arguments of the program
        """
        parser = argparse.ArgumentParser(description='Npuzzle program.')
        parser.add_argument('-f', '--file', help='input rules file',
                            required=True)
        res = parser.parse_args(args)
        self.file = res.file

    def check_file(self):
        if not Path(self.file).is_file():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                    self.file)

        with open(self.file, 'r') as file:
            for line in file.readlines():
                if line.startswith('#'):
                    continue
                rule = line.split('#')[0]
                if rule.isspace():
                    continue
                self.instructions.append(rule.strip())
