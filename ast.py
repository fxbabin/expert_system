class Node_letter(object):
    
    def __init__(self, token, name):
        self.token = token
        self.name = name
        self.state = 0
        self.neg = 0
        self.childs_pos = []
        self.childs_neg = []
        
    def __str__(self):
        return "Node_letter({})".format(self.token)
        
class Node_condition(object):
    
    def __init__(self, left, cond, right):
        self.left = left
        self.token = self.cond = cond
        self.right = right
        self.neg = 0
        
    def __str__(self):
        return "Node_condition({}".format(self.token)
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
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()
