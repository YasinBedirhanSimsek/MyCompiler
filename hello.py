from sly import Lexer

class CalcLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { ID, NUMBER, PLUS, MINUS, TIMES,
               DIVIDE, ASSIGN, LPAREN, RPAREN, LCURLY, RCURLY, IF, OR, GREATERTHAN, AND, NOTEQUAL }

    # String containing ignored characters (between tokens)
    ignore = ' \t'

    # Other ignored patterns
    ignore_comment = r'\#.*'
    ignore_newline = r'\n+'

    # Regular expression rules for tokens
    
    ID      = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER  = r'\b(0x[0-9a-fA-F]+|[0-9]+)\b'
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    ASSIGN  = r'='
    LPAREN  = r'\('
    RPAREN  = r'\)'
    LCURLY = r'\{'
    RCURLY = r'\}'
    IF = r'if'
    # EQUAL = r'\==' #equal does not work it see only one "=" symbol
    GREATERTHAN = r'<='
    OR = r'\|'
    AND = r'\&'
    NOTEQUAL = r'!='


if __name__ == '__main__':
    data = '''x = 3 + 0x42 anan
                * (s    # This is a comment
                    - t) if { asd } | & !='''
    lexer = CalcLexer()

    token_list = []

    for tok in lexer.tokenize(data):
        token_list.append(tok)
        print(tok)


