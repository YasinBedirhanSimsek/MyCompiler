from sly.lex import Token
from Lex import CalcLexer
from Yacc import CalcParser

#Function

#text = '''if (3==5) { 3 + 2 } else if (3==4) { 1*1 } else if (3==1) { 49 } else { 3 * 2 }'''

#text0 = '''function asd (a, b, c) { a = 5 + 1}'''
#text1 = '''x = 0'''
#text2 = '''y = 1'''
#text3 = '''z = 2 '''
#text4 = '''asd (x, y, z)'''
#text5 = '''x'''

text = ''' '''

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
