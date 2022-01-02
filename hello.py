from sly.lex import Token
from Lex import CalcLexer
from Yacc import CalcParser

#TO-DO:
#String
#If
#While
#Function

if __name__ == '__main__':
                 
    lexer  = CalcLexer()
    parser = CalcParser()

    while True:
        try:
            text = input('calc > ')
            result = parser.parse(lexer.tokenize(text))
        except EOFError:
            break
