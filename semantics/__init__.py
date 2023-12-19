import math
from matplotlib import pyplot as plt
from parser.parser import *
from parser.expression import *


class Semantics:
    def __init__(self, parser: Parser):
        self.parser = parser
        self.origin_x = 0
        self.origin_y = 0
        self.scale_x = 1
        self.scale_y = 1
        self.rot_degree = 0
        self.t = 0
        self.statements = []

    def parse(self):
        self.parser.program()

        self.origin_x = calculate_expr_tree(self.parser.origin_x)
        self.origin_y = calculate_expr_tree(self.parser.origin_y)
        self.scale_x = calculate_expr_tree(self.parser.scale_x)
        self.scale_y = calculate_expr_tree(self.parser.scale_y)
        self.rot_degree = calculate_expr_tree(self.parser.rot_degree)
        self.statements = self.parser.statements

    def run(self):
        for statement in self.statements:
            self.draw(statement)
        plt.show()

    def draw(self, statement):
        low_bound = calculate_expr_tree(statement.low_bound)
        high_bound = calculate_expr_tree(statement.high_bound)
        step = calculate_expr_tree(statement.step)
        self.t = low_bound
        _x = []
        _y = []
        while self.t <= high_bound:
            ExprNode.parameter = self.t
            x = calculate_expr_tree(statement.x_value)
            y = calculate_expr_tree(statement.y_value)
            x = x * self.scale_x + self.origin_x
            y = y * self.scale_y + self.origin_y
            x1 = x * math.cos(self.rot_degree) - y * math.sin(self.rot_degree)
            y1 = x * math.sin(self.rot_degree) + y * math.cos(self.rot_degree)
            _x.append(x1)
            _y.append(y1)
            self.t = self.t + step
        plt.plot(_x, _y)
