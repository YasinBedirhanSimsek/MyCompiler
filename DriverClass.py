from sly.lex import Token
from Lex import CalcLexer
from Yacc import CalcParser

if __name__ == '__main__':
                 
    lexer  = CalcLexer()
    parser = CalcParser()

    lines = None

    with open('code.txt') as f:
        lines = f.read()

    while True:
        try:
            #text = input('calc > ')
            result = parser.parse(lexer.tokenize(lines))
            break
        except Exception as e:
            print(e)
            break
