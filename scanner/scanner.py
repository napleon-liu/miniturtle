from scanner.token import *
from scanner.dfa import *
from math import *


def is_space(char):
    return char == ' ' or char == '\t' or char == '\n' or char == '\r' or char == '\v' or char == '\f'


class Scanner(object):
    _token_table = [
        Token(TokenType.CONST_ID, "PI", 3.1415926, 0),
        Token(TokenType.CONST_ID, "E", 2.71828, 0),
        Token(TokenType.T, "T", 0.0, 0),
        Token(TokenType.FUNC, "SIN", 0.0, id(sin)),
        Token(TokenType.FUNC, "COS", 0.0, id(cos)),
        Token(TokenType.FUNC, "TAN", 0.0, id(tan)),
        Token(TokenType.FUNC, "LN", 0.0, id(log)),
        Token(TokenType.FUNC, "EXP", 0.0, id(exp)),
        Token(TokenType.FUNC, "SQRT", 0.0, id(sqrt)),
        Token(TokenType.ORIGIN, "ORIGIN", 0.0, 0),
        Token(TokenType.SCALE, "SCALE", 0.0, 0),
        Token(TokenType.ROT, "ROT", 0.0, 0),
        Token(TokenType.IS, "IS", 0.0, 0),
        Token(TokenType.FOR, "FOR", 0.0, 0),
        Token(TokenType.FROM, "FROM", 0.0, 0),
        Token(TokenType.TO, "TO", 0.0, 0),
        Token(TokenType.STEP, "STEP", 0.0, 0),
        Token(TokenType.DRAW, "DRAW", 0.0, 0),
        Token(TokenType.COLOR, "COLOR", 0.0, 0),
        Token(TokenType.PIXSIZE, "PIXSIZE", 0.0, 0),
    ]

    _dfa = DFA()

    def __init__(self, file_path: str):
        self.file = open(file_path, "r")
        self.token = Token(TokenType.NONETOKEN, "", 0.0, 0)

    def __del__(self):
        self.file.close()

    def get_token(self):
        return self.token

    '''
    1. 预处理，跳过空白字符
    2. 边扫描输入，边转移状态
    3. 根据终态所标记的记号种类信息，进行特殊处理
    '''

    def read_token(self) -> Token:
        while True:
            self.token = Token(TokenType.NONETOKEN, "", 0.0, 0)
            try:
                curr_char = self.pre_process()
            except EOFError:
                self.token.type = TokenType.NONETOKEN
                return self.token
            last_state = self.scan_move(curr_char)
            to_be_continue = self.post_process(last_state)
            if not to_be_continue:
                break
        if self.token.type == TokenType.NONETOKEN:
            print("Error: Unknown token: " + self.token.lexeme)
            return False
        elif self.token.lexeme == "":
            return False
        return True
    '''
    边扫描输入，边转移状态
    '''

    def scan_move(self, curr_char):
        curr_state = self._dfa.get_start_state()
        while True:
            next_state = self._dfa.move(curr_state, curr_char)
            if next_state == -1:
                self.unread_char(curr_char)
                break
            self.token.lexeme += curr_char
            curr_state = next_state
            try:
                curr_char = self.read_char()
            except EOFError:
                break

        return curr_state

    '''
    从文件中读取一个字符，如果到达文件末尾则抛出EOFError
    '''

    def pre_process(self):
        curr_char: str
        while True:
            curr_char = self.read_char()
            if not is_space(curr_char):
                return curr_char

    def read_char(self):
        next_char = self.file.read(1)
        if next_char == '':
            raise EOFError
        else:
            return next_char.upper()

    '''
    将文件指针回退一个字符, 如果回退到文件开头则抛出EOFError
    '''

    def unread_char(self, ch):
        if ch == '' or ch == '\n':
            return
        else:
            self.file.seek(self.file.tell() - 1)

    def post_process(self, last_state) -> bool:
        to_be_continue = False
        token_type: TokenType
        self.token.type = token_type = self._dfa.accept(last_state)
        if token_type == TokenType.ERRTOKEN:
            raise Exception("Unknown token: " + self.token.lexeme)
        elif token_type == TokenType.ID:
            if not self.query_token_table():
                self.token.type = TokenType.NONETOKEN
        elif token_type == TokenType.CONST_ID:
            self.token.value = float(self.token.lexeme)
        elif token_type == TokenType.COMMENT:
            while True:
                curr_char = self.read_char()
                if curr_char == '\n':
                    break
            to_be_continue = True
        else:
            self.token.value = 0.0
            self.token.func_ptr = 0
        return to_be_continue

    def query_token_table(self) -> bool:
        for token in self._token_table:
            if token.lexeme == self.token.lexeme:
                self.token.type = token.type
                self.token.value = token.value
                self.token.func_ptr = token.func_ptr
                return True
        return False
