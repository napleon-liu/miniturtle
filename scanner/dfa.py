from scanner.token import TokenType


class DFA(object):
    final_states = {
        1: TokenType.ID,
        2: TokenType.CONST_ID,
        3: TokenType.CONST_ID,
        4: TokenType.MUL,
        5: TokenType.DIV,
        6: TokenType.POWER,
        7: TokenType.PLUS,
        8: TokenType.MINUS,
        9: TokenType.SEMICOLON,
        10: TokenType.L_BRACKET,
        11: TokenType.R_BRACKET,
        12: TokenType.COMMA,
        13: TokenType.COMMENT
    }

    transfer_table = {
        (0, "alpha"): 1,
        (0, "digit"): 2,
        (0, "*"): 4,
        (0, "/"): 6,
        (0, "-"): 7,
        (0, "+"): 8,
        (0, ","): 9,
        (0, ";"): 10,
        (0, "("): 11,
        (0, ")"): 12,
        (1, "alpha"): 1,
        (1, "digit"): 1,
        (2, "digit"): 2,
        (2, "."): 3,
        (3, "digit"): 3,
        (4, "*"): 4,
        (6, "/"): 13,
        (7, "-"): 13,
    }

    # 初始化
    def __init__(self):
        self.start_state = 0

    # 状态转移
    def move(self, state, char: str):
        if char.isalpha():
            char = "alpha"
        elif char.isdigit():
            char = "digit"

        if self.transfer_table.get((state, char)):
            return self.transfer_table.get((state, char))
        else:
            return -1

    # 终态判断
    def accept(self, state) -> TokenType:
        if self.final_states.get(state):
            return self.final_states.get(state)
        return TokenType.ERRTOKEN

    def get_start_state(self):
        return self.start_state
