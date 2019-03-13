class Node_letter(object):

    def __init__(self, token, name):
        self.token = token
        self.name = name
        self.state = 0
        self.neg = 0
        self.childs_pos = []
        self.childs_neg = []
        self.visited = 0
        self.or_dic = {}
        self.xor_dic = {}
        self.ind = 0

    def __str__(self):
        return "Node_letter({})".format(self.token)


class Node_condition(object):

    def __init__(self, left, cond, right):
        self.left = left
        self.token = self.cond = cond
        self.right = right
        self.neg = 0
        self.visited = 0
        self.or_dic = {}
        self.xor_dic = {}
        self.ind = 0

    def __str__(self):
        return "Node_condition({}".format(self.token)
