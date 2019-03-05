from xs_node import Node_condition, Node_letter


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.gen = self.lexer.get_next_token()
        self.current_token = next(self.gen)

    def error(self, s):
        raise Exception("Invalid syntax : {}".format(s))

    def get_next_token(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = next(self.gen)
        else:
            self.error("could not find match of parenthesis")

    def parse(self):
        """
        Cette fonction a pour but d'enclencher le debut du parsing recursif.
        la variable node va etre le neud representant la racine de l'AST.
        """
        node = self.deep_one()
        if self.current_token.type != "EOL":
            self.error(self.lexer.error())
        if (node.token.type != "IMPLIES") and (node.token.type != "ONLY_IF"):
            self.error("Missing valid equals sign")
        self.check_implies(node.left)
        return node

    def check_implies(self, node):
        if node:
            if ((node.token.type == "IMPLIES") or
                    (node.token.type == "ONLY_IF")):
                self.error("Too many equals signs")
            if type(node).__name__ == "Node_condition":
                self.check_implies(node.left)
                self.check_implies(node.right)

    def deep_one(self):
        """
        Cette pronfondeur de prioritée est assignée aux token suivants :
            Token(IMPLIES, '=>')
            Token(ONLY_IF, '<=>')
            Token(NEG, '!')
        """
        node = self.deep_two()
        while self.current_token.type in ("IMPLIES", "ONLY_IF"):
            token = self.current_token
            if token.type == "IMPLIES":
                self.get_next_token("IMPLIES")
            if token.type == "ONLY_IF":
                self.get_next_token("ONLY_IF")
            node = Node_condition(left=node, cond=token, right=self.deep_two())
        return node

    def deep_two(self):
        """
        Cette profondeur de prioritée est assignée aux token suivants :
            Token(AND, '+')
            Token(OR, '|')
            Token(XOR, '^')
        """
        node = self.deep_three()
        while self.current_token.type in ("AND", "OR", "XOR"):
            token = self.current_token
            if token.type == "AND":
                self.get_next_token("AND")
            if token.type == "OR":
                self.get_next_token("OR")
            if token.type == "XOR":
                self.get_next_token("XOR")

            node = (Node_condition(left=node,
                    cond=token, right=self.deep_three()))
        return node

    def deep_three(self):
        """
        Cette profondeur de prioritée est assignée au token equals :
            Token(LETTER, 'A->Z')
            Token(OPEN_PAR, '(' )
            Token(CLOSE_PAR, ')' )
            Token(NOT, '!')
        """
        token = self.current_token
        if token.type == "LETTER":
            self.get_next_token("LETTER")
            return Node_letter(token, token.value)
        elif token.type == "OPEN_PAR":
            self.get_next_token("OPEN_PAR")
            node = self.deep_one()
            self.get_next_token("CLOSE_PAR")
            return node
        elif token.type == "NOT":
            self.get_next_token("NOT")
            token = self.current_token
            if token.type == "LETTER":
                self.get_next_token("LETTER")
                ret = Node_letter(token, token.value)
                ret.neg = 1
                return ret
            elif token.type == "OPEN_PAR":
                self.get_next_token("OPEN_PAR")
                node = self.deep_one()
                node.neg = 1
                self.get_next_token("CLOSE_PAR")
                return node
        else:
            self.lexer.error()
