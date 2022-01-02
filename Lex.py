from sly import Lexer
from sly.lex import Token

class CalcLexer(Lexer):
    # Set of token names. This is always required
    tokens = { 
        
        #Objects
        ID, NUMBER,
         
        #SYMBOLS
        LPAREN, RPAREN,
        
        LCURLY, RCURLY,
        
        #OPERATIONS
        PLUS, MINUS, TIMES, DIVIDE, ASSIGN,
        
        BITWISE_OR, BITWISE_AND, BITWISE_NOT,
        
        #LOGIC
        #GREATER_THAN, GREATER_THAN_EQ, LOWER_THAN, LOWER_THAN_EQ,
        BIGGER, SMALLER,
        
        IS_EQUAL, IS_NOT_EQUAL,
        
        #CONDITIONAL
        IF, ELSE_IF, ELSE,

        #LOOPS
        WHILE, FOR, BREAK  
    }

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
    
    LCURLY  = r'\{'
    RCURLY  = r'\}'

    #OPERATIONS
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    ASSIGN  = r'='

    BITWISE_OR  = r'\|'
    BITWISE_AND = r'\&'
    BITWISE_NOT = r'\!'

    #LOGIC
    #GREATER_THAN_EQ   = r'>='
    #GREATER_THAN      = r'>'
    BIGGER = r'(>=|>)'

    
    #LOWER_THAN_EQ  = r'<='
    #LOWER_THAN     = r'<'
    SMALLER = r'(<=|<)'

    IS_EQUAL     = r'\?='
    IS_NOT_EQUAL = r'\!='

    #CONDITIONAL
    ID['if']      = IF
    ID['else if'] = ELSE_IF
    ID['else']    = ELSE

    #LOOPS
    ID['while'] = WHILE    
    ID['for']   = FOR 
    ID['break'] = BREAK


    ############################################################

    def NUMBER(self, t:Token):
        t.value = int(t.value)
        return t

    