from es_token import Token


class Lexer(object):
    def __init__(self, line):
        self.rule = line
        self.pos = 0

    def error(self, EOL=False):
        if EOL is False:
            raise Exception(('Invalid character \'{}\' at index {}'
                             .format(self.rule[self.pos], self.pos + 1)))
        else:
            raise Exception('Invalid character \'{}\' at index {}'
                            .format("EOL", self.pos + 1))

    def get_next_token(self):
        op = {
            "+": "AND",
            "|": "OR",
            "^": "XOR",
            "!": "NOT",
            "(": "OPEN_PAR",
            ")": "CLOSE_PAR"
        }
        op_eq = {
            "=": "EQUAL",
            ">": "IMPLIES",
            "<": "ONLY_IF"
        }
        i = 0
        len_rule = len(self.rule)
        while i < len_rule:
            self.pos = i
            if self.rule[i] == " ":
                i += 1
                continue
            if self.rule[i].isupper() and self.rule[i].isalpha():
                yield Token("LETTER", self.rule[i])
            elif self.rule[i] in op:
                yield Token(op[self.rule[i]], self.rule[i])
            elif self.rule[i] in op_eq:
                tmp = self.get_equals_token(i, len_rule)
                i += tmp[0]
                yield tmp[1]
            else:
                self.error()
            i += 1
        yield Token("EOL", None)

    def get_equals_token(self, i, len_rule):
        if self.rule[i] == "<" and i < len_rule - 2:
            if self.rule[i + 1] == "=":
                if self.rule[i + 2] == ">":
                    return ([2, Token("ONLY_IF", "<=>")])
                else:
                    self.pos += 2
                    self.error()
            else:
                self.pos += 1
                self.error()
        elif self.rule[i] == "=" and i < len_rule - 1:
            if self.rule[i + 1] == ">":
                return ([1, Token("IMPLIES", "=>")])
            else:
                self.pos += 1
                self.error()
        if i == len_rule - 1:
            self.pos += 1
            self.error(EOL=True)
        elif i == len_rule - 2:
            self.pos += 2
            self.error(EOL=True)
        self.error()

    def lexer_tester(self):
        out = ""
        for e in self.get_next_token():
            if e.value is None:
                out += "."
            else:
                out += e.value
        return (out)
