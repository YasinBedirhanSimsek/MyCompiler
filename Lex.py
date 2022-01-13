from sly import Lexer
from sly.lex import Token
from sympy import true

class CalcLexer(Lexer):
    # Set of token names. This is always required
    tokens = { 
        
        #Objects
        ID, NUMBER, 
         
        #SYMBOLS
        LPAREN, RPAREN, SEMI_COL,
        
        LCURLY, RCURLY, COMMA, 
        
        #OPERATIONS
        PLUS, MINUS, TIMES, DIVIDE, ASSIGN, MOD, EXPONENT, 
        
        BITWISE_OR, BITWISE_AND,
        
        #LOGIC
        GREATER_THAN, GREATER_THAN_EQ, LESS_THAN, LESS_THAN_EQ,

        OR, AND, IS_NOT_EQUAL, IS_EQUAL,

        #LOOP
        WHILE, LOOP_BREAK,

        #CONDITIONAL
        IF, ELSE,

        #FUNCTION
        FUNCTION
    }

    literals = {'\n'}

    # String containing ignored characters (between tokens)
    ignore = ' \t'
    ignore_comment = r'\#.*'
    ignore_newline = r'\n+'

    # Regular expression rules for tokens

    #Objects  
    ID      = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER  = r'[+-]?([0-9]*[.])?[0-9]+'

    #STRING  = r'\".*\"'

    #SYMBOLS
    LPAREN  = r'\('
    RPAREN  = r'\)'
    
    LCURLY   = r'\{'
    RCURLY   = r'\}'
    COMMA    = r'\,'
    SEMI_COL = r';'

    #MATHEMATICAL OPERATIONS
    PLUS     = r'\+'
    MINUS    = r'-'
    EXPONENT = r'\*\*' 
    TIMES    = r'\*'
    DIVIDE   = r'/'
    MOD      = r'%'
    
    #BITWISE OPERATIONS
    BITWISE_OR  = r'\|'
    BITWISE_AND = r'\&'

    #LOGICAL CHECKS
    GREATER_THAN_EQ = r'>='
    GREATER_THAN    = r'>'
    LESS_THAN_EQ   = r'<='
    LESS_THAN      = r'<'

    IS_EQUAL     = r'==' 
    IS_NOT_EQUAL = r'\!='

    #ASSIGNMENT
    ASSIGN   = r'='

    #CONDITIONAL
    ID['if']   = IF
    ID['else'] = ELSE
    ID['or']   = OR
    ID['and']  = AND

    #LOOPS
    ID['while'] = WHILE
    ID['break'] = LOOP_BREAK

    #Function
    ID['function'] = FUNCTION

    ############################################################

    #Match Action
    def NUMBER(self, t:Token):      
        try:
            t.value = int(t.value)
            return t
        except:
            pass

        try:
            t.value = float(t.value)
            return t
        except:
            return None

    # Define a rule so we can track line numbers
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # Compute column.
    # input is the input text string
    # token is a token instance
    def find_column(text, token):
        last_cr = text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        column = (token.index - last_cr) + 1
        return column
    
    # Error handling rule
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1