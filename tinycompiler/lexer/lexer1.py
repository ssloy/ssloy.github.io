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
            elif sym1 == '"':               # start a string scan
                state = 3
            elif sym1 not in ['\r', '\t', ' ', '\n']: # ignore whitespace
                raise Exception(f'Lexical error: illegal character "{sym1}"')
        elif state==2:                          # scanning a number
            if sym1.isdigit():                  # is next character a digit?
                accum += sym1                   # if yes, continue
            else:
                yield Token('INTEGER', accum)   # otherwise, emit number token
                idx -= 1
                state, accum = 0, ''            # start new scan
        elif state==3:                                          # scanning a string, check next character
            if sym1 != '"' or accum and accum[-1]=='\\':        # if not quote mark (or if escaped quote mark),
                accum += sym1                                   # continue the scan
            else:
                yield Token('STRING', accum)                    # otherwise emit the token
                state, accum = 0, '' # start new scan
        if sym1 == '\n':
            if state==1: # if comment, start new scan
                state, accum = 0, ''
        idx += 1
    if state:
        print(state,accum)
        raise Exception('Lexical error: unexpected EOF')

tokens = list(tokenize('''0 // this is a comment to ignore by the lexer
"this is a string with an escaped quotation mark \\" and double slash // that is not considered as a comment"
1337
'''))
print([t for t in tokens])
