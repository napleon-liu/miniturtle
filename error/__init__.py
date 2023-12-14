from scanner.token import *


class Error:
    def __init__(self, token):
        self.token = token

    def syntax_error(self, error_type):
        if error_type == 1:
            print("Syntax Error: Unknown token: " + self.token.lexeme)
        elif error_type == 2:
            print("Syntax Error: Match Token Error,Expected TokenType:" + str(self.token.type))
