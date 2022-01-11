from sly import Lexer
from sly.lex import Token

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
        GREATER_THAN, GREATER_THAN_EQ, LOWER_THAN, LOWER_THAN_EQ,

        OR, AND, IS_NOT_EQUAL, IS_EQUAL,

        #LOOP
        WHILE,

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
    NUMBER  = r'\d+'

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
    LOWER_THAN_EQ   = r'<='
    LOWER_THAN      = r'<'

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

    #Function
    ID['function'] = FUNCTION

    ############################################################

    #Match Action
    def NUMBER(self, t:Token):
        t.value = int(t.value)
        return t