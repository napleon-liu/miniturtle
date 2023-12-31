from error import Error
from parser.expression import *
from scanner.scanner import Scanner
from scanner.token import *


class DrawStatement:
    def __init__(self):
        self.low_bound = None
        self.high_bound = None
        self.x_value = None
        self.y_value = None
        self.step = None


class Parser:
    parameter = 0.0

    def __init__(self, file_path: str):
        self.origin_x = 0
        self.origin_y = 0
        self.scale_x = 1
        self.scale_y = 1
        self.t = 0
        self.rot_degree = 0
        self.statements = []
        self.scanner = Scanner(file_path)
        self.token = Token(TokenType.NONETOKEN, "", 0.0, 0)
        self.error = Error(self.token)
        self.fetch_token()

    def fetch_token(self):
        self.scanner.read_token()
        self.token = self.scanner.get_token()
        if self.token.type == TokenType.NONETOKEN:
            self.error.syntax_error(1)

    def program(self):
        print("enter in program")
        while self.token.type != TokenType.NONETOKEN:
            self.statement()
            self.match_token(TokenType.SEMICOLON)
        print("exit from program")

    def statement(self):
        print("  enter in statement")
        if self.token.type == TokenType.ORIGIN:
            self.origin_statement()
        elif self.token.type == TokenType.SCALE:
            self.scale_statement()
        elif self.token.type == TokenType.ROT:
            self.rot_statement()
        elif self.token.type == TokenType.FOR:
            self.for_statement()
        else:
            self.error.syntax_error(2)
        print("  exit from statement")

    def match_token(self, token_type: TokenType):
        if self.token.type != token_type:
            self.error.syntax_error(2)
        print("      match token: " + self.token.lexeme)
        self.fetch_token()

    '''
    // OriginStatement -> ORIGIN IS
    // L_BRACKET Expression COMMA Expression R_BRACKET
    // origin is (200, 300)
    '''

    def origin_statement(self):
        print("    enter in origin_statement")
        self.match_token(TokenType.ORIGIN)
        self.match_token(TokenType.IS)
        self.match_token(TokenType.L_BRACKET)
        self.origin_x = self.expression()
        self.match_token(TokenType.COMMA)
        self.origin_y = self.expression()
        self.match_token(TokenType.R_BRACKET)
        print("    exit from origin_statement")

    '''
    // ScaleStatement  → SCALE IS
    // L_BRACKET Expression COMMA Expression R_BRACKET
    // scale is (2, 1) -- 设置横纵坐标缩放比例
    '''

    def scale_statement(self):
        print("    enter in scale_statement")
        self.match_token(TokenType.SCALE)
        self.match_token(TokenType.IS)
        self.match_token(TokenType.L_BRACKET)
        self.scale_x = self.expression()
        self.match_token(TokenType.COMMA)
        self.scale_y = self.expression()
        self.match_token(TokenType.R_BRACKET)
        print("    exit from scale_statement")

    '''
    // RotStatement → ROT IS Expression
    // rot is pi/6  -- 设置旋转角度
    '''

    def rot_statement(self):
        print("    enter in rot_statement")
        self.match_token(TokenType.ROT)
        self.match_token(TokenType.IS)
        self.rot_degree = self.expression()
        print("    exit from rot_statement")

    def for_statement(self):
        print("    enter in for_statement")
        statement = DrawStatement()
        self.match_token(TokenType.FOR)
        self.match_token(TokenType.T)
        self.match_token(TokenType.FROM)
        statement.low_bound = self.expression()
        self.match_token(TokenType.TO)
        statement.high_bound = self.expression()
        self.match_token(TokenType.STEP)
        statement.step = self.expression()
        self.match_token(TokenType.DRAW)
        self.match_token(TokenType.L_BRACKET)
        statement.x_value = self.expression()
        self.match_token(TokenType.COMMA)
        statement.y_value = self.expression()
        self.match_token(TokenType.R_BRACKET)
        self.statements.append(statement)
        print("    exit from for_statement")

    '''
    ExprNode *left, *right;
    Token_Type token_temp;
    left = Term();
    while (token.token_type == PLUS || token.token_type == MINUS)
    {
        token_temp = token.token_type;
        MatchToken(token_temp);
        right = Term();
        left = MakeExprNode(token_temp, left, right);
    }
    return left;
    
    '''

    def expression(self):
        print("      enter in expression")
        left = self.term()
        while self.token.type == TokenType.PLUS or self.token.type == TokenType.MINUS:
            token_temp = self.token.type
            self.match_token(token_temp)
            right = self.term()
            left = ExprNode(token_temp, left, right)
        print("      left from expression")
        print_expr_tree(left)
        return left

    '''
    ExprNode *left, *right;
    Token_Type token_temp;
    left = Factor();
    while (token.token_type == MUL || token.token_type == DIV)
    {
        token_temp = token.token_type;
        MatchToken(token_temp);
        right = Factor();
        left = MakeExprNode(token_temp, left, right);
    }
    return left;
    '''

    def term(self):
        left = self.factor()
        while self.token.type == TokenType.MUL or self.token.type == TokenType.DIV:
            token_temp = self.token.type
            self.match_token(token_temp)
            right = self.factor()
            left = ExprNode(token_temp, left, right)
        return left

    '''
    ExprNode *node = NULL;
    Token_Type token_temp;

    if (token.token_type == PLUS || token.token_type == MINUS)
    {
        token_temp = token.token_type;
        MatchToken(token_temp);
        node = Factor();
        node = MakeExprNode(token_temp, node, NULL); // 创建一个带有正负号的表达式节点
    }
    else
    {
        node = Component();
    }

    return node;
    '''

    def factor(self):
        if self.token.type == TokenType.PLUS or self.token.type == TokenType.MINUS:
            token_temp = self.token.type
            self.match_token(token_temp)
            node = self.factor()
            node = ExprNode(token_temp, ExprNode(TokenType.CONST_ID, 0.0), node)
        else:
            node = self.component()
        return node

    '''
    ExprNode *node = Atom();

    if (token.token_type == POWER)
    {
        MatchToken(POWER);
        ExprNode *right = Component();
        node = MakeExprNode(POWER, node, right); // 创建一个带有幂运算的表达式节点
    }

    return node;    
    '''

    def component(self):
        node = self.atom()
        if self.token.type == TokenType.POWER:
            self.match_token(TokenType.POWER)
            right = self.component()
            node = ExprNode(TokenType.POWER, node, right)
        return node

    '''
    ExprNode *node;
    switch (token.token_type)
    {
    // 常数节点
    case CONST_ID:
        MatchToken(CONST_ID);
        node = MakeExprNode(CONST_ID, token.value);
        break;
    case T:
        MatchToken(T);
        node = MakeExprNode(T);
        break;
    case FUNC:
        // 函数调用结点
        MatchToken(FUNC);
        MatchToken(L_BRACKET);
        struct ExprNode *child = Expression();
        MatchToken(R_BRACKET);
        node = MakeExprNode(FUNC, token.FuncPtr, child);
    case L_BRACKET:
        // 括号表达式结点
        MatchToken(L_BRACKET);
        node = Expression();
        MatchToken(R_BRACKET);
    default:
        break;
    }
    '''

    def atom(self):
        node: ExprNode
        if self.token.type == TokenType.CONST_ID:
            token = self.token
            self.match_token(TokenType.CONST_ID)
            node = ExprNode(TokenType.CONST_ID, token.value)
        elif self.token.type == TokenType.T:
            self.match_token(TokenType.T)
            node = ExprNode(TokenType.T, self.parameter)
        elif self.token.type == TokenType.FUNC:
            func = self.token.func_ptr
            self.match_token(TokenType.FUNC)
            self.match_token(TokenType.L_BRACKET)
            child = self.expression()
            self.match_token(TokenType.R_BRACKET)
            node = ExprNode(TokenType.FUNC, func, child)
        elif self.token.type == TokenType.L_BRACKET:
            self.match_token(TokenType.L_BRACKET)
            node = self.expression()
            self.match_token(TokenType.R_BRACKET)
        else:
            self.error.syntax_error(2)
        return node
