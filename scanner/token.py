import enum
import string


class TokenType(enum.Enum):
    ID = 1,  # 标识符
    COMMENT = 2,  # 注释
    ORIGIN = 3,  # 原点
    SCALE = 4,  # 比例
    ROT = 5,  # 旋转
    IS = 6,  # 赋值
    TO = 7,  # 到
    STEP = 8,  # 步长
    DRAW = 9,  # 画图
    FOR = 10,  # 循环
    FROM = 11,  # 从
    T = 12,  # 参数
    SEMICOLON = 13,  # 分号
    L_BRACKET = 14,  # 左括号
    R_BRACKET = 15,  # 右括号
    COMMA = 16,  # 逗号
    PLUS = 17,  # 加
    MINUS = 18,  # 减
    MUL = 19,  # 乘
    DIV = 20,  # 除
    POWER = 21,  # 幂
    FUNC = 22,  # 函数
    CONST_ID = 23,  # 常数
    NONETOKEN = 24,  # 空记号
    PIXSIZE = 25,  # 画笔大小
    COLOR = 26,  # 画笔颜色
    ERRTOKEN = 27,  # 出错记号

    def __init__(self):
        pass


class Token(object):
    def __init__(self, token_type: TokenType, token_lexeme: string, token_value: float, token_func_ptr: int):
        self.type = token_type
        self.lexeme = token_lexeme
        self.value = token_value
        self.func_ptr = token_func_ptr


