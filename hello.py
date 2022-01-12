from sly.lex import Token
from Lex import CalcLexer
from Yacc import CalcParser

#Function

text = '''
if(3 + 2) {
    a=3;
}
'''

if __name__ == '__main__':
                 
    lexer  = CalcLexer()
    parser = CalcParser()

    while True:
        try:
            #text = input('calc > ')
            result = parser.parse(lexer.tokenize(text))
            break
        except Exception as e:
            print(e)
            break
