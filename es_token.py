
class Token(object):
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(NEG, "!")
            Token(LETTER, "A")
            Token(AND, '+')
            Token(OR, '|')
            Token(XOR, '^')
        """
        return 'Token({}, {})'.format(
            self.type,
            self.value
        )
