from sly.lex import Token
from Lex import CalcLexer
from Yacc import CalcParser

#Function

#text = '''if (3==5) { 3 + 2 } else if (3==4) { 1*1 } else if (3==1) { 49 } else { 3 * 2 }'''

if __name__ == '__main__':
                 
    lexer  = CalcLexer()
    parser = CalcParser()

    while True:
        try:
            text = input('calc > ')
            result = parser.parse(lexer.tokenize(text))
        except EOFError:
            break
