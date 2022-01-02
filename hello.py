from sly.lex import Token
from Lex import CalcLexer
from sly import Lexer

if __name__ == '__main__':

    data = '''
    
    #define a
    a = 2 + 3

    #define b
    b = a + 5

    while(b >= 0)
        a = a - 1

        if(a ?= 0)
            break

    

    '''
                 
    lexer = CalcLexer()

    token_list = []

    for tok in lexer.tokenize(data):
        token_list.append(tok)

    tok : Token
    for tok in token_list:
        print('(%r, %r)\n' %(tok.type, tok.value) )

