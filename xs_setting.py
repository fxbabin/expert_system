
##################
#   Librairies   #
##################

from pathlib import Path
import argparse
import sys
import errno
import os

#############
#   Class   #
#############


class Setting:

    def __init__(self):
        self.file = ""
        self.graph_rules = ""
        self.rules = []
        self.true_facts = ""
        self.queries = ""
        self.interactive = False
        self.truth_tables = False
        self.get_arguments(sys.argv[1:])
        self.check_file()

    def error(self, s):
        raise Exception("Invalid syntax : {}".format(s))

    def get_arguments(self, args=None):
        """
        Check the input arguments of the program
            :param args=None: arguments of the program
        """
        parser = argparse.ArgumentParser(description='Npuzzle program.')
        parser.add_argument('-f', '--file', help='input rules file',
                            required=True)
        parser.add_argument('-g', '--graph',
                            help='graphs you want to generate')
        parser.add_argument('-t', '--truth_tables', action="store_true",
                            help='display truth tables used for resolution')
        parser.add_argument('-i', '--interactive_facts', action="store_true",
                            help='interactive facts mode')
        res = parser.parse_args(args)
        self.file = res.file
        self.graph_rules = res.graph 
        self.interactive = res.interactive_facts
        self.truth_tables = res.truth_tables

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
                if rule[0] == "=":
                    if len(self.rules) == 0:
                        self.error("facts declared but no rules are found")
                    self.true_facts = rule[1:].strip()
                elif rule[0] == "?":
                    if len(self.rules) == 0:
                        self.error("queries declared but no rules are found")
                    if len(self.true_facts) == 0:
                        self.error("queries declared but no facts are found")
                    self.queries = rule[1:].strip()
                else:
                    if len(self.true_facts) > 0:
                        self.error("rule declared but facts are already"
                                   "declared")
                    if len(self.queries) > 0:
                        self.error("rule declared but queries are already"
                                   "declared")
                    self.rules.append(rule.strip())
