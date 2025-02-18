from sly import Parser
from lexer import WendLexer
from syntree import *

class WendParser(Parser):
    tokens = WendLexer.tokens
    precedence = (
         ('left', PLUS, MINUS),
         ('left', TIMES),
    )

    @_('ID ASSIGN expr SEMICOLON')
    def statement(self, p):
        return Assign(p[0], p.expr, {'lineno':p.lineno})

    @_('expr PLUS expr',
       'expr MINUS expr',
       'expr TIMES expr')
    def expr(self, p):
        return ArithOp(p[1], p.expr0, p.expr1, {'lineno':p.lineno})

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('ID')
    def expr(self, p):
        return Var(p[0], {'lineno':p.lineno})

    @_('INTVAL')
    def expr(self, p):
        return Integer(int(p.INTVAL), {'lineno':p.lineno})

    def error(self, token):
        if not token:
            raise Exception('Syntax error: unexpected EOF')
        raise Exception(f'Syntax error at line {token.lineno}, token={token.type}')
