class Token:
    def __init__(self, t, v):
        self.type, self.value = t, v

    def __repr__(self):
         return f'{self.type}({self.value})'

def tokenize(text):
    idx, state, accum = 0, 0, ''
    while idx<len(text):
        sym1 = text[idx+0] if idx<len(text)-0 else ' ' # current symbol
        sym2 = text[idx+1] if idx<len(text)-1 else ' ' # next symbol
        if state==0: # start scanning a new token
            if sym1 == '/' and sym2 == '/': # start a comment scan
                state = 1
            elif sym1.isdigit():            # start a number scan
                state = 2
                accum += sym1
            elif sym1 not in ['\r', '\t', ' ', '\n']: # ignore whitespace
                raise Exception(f'Lexical error: illegal character "{sym1}"')
        elif state==2:                          # scanning a number
            if sym1.isdigit():                  # is next character a digit?
                accum += sym1                   # if yes, continue
            else:
                yield Token('INTEGER', accum)   # otherwise, emit number token
                idx -= 1
                state, accum = 0, ''            # start new scan
        if sym1 == '\n':
            if state==1: # if comment, start new scan
                state, accum = 0, ''
        idx += 1

tokens = list(tokenize('''0 // this is a comment to ignore by the lexer
1337
'''))
print([t for t in tokens])
