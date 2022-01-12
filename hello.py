text = '''

result = 0;

qwer = 3, tre = 4;

function max(num1, num2) {

    if (num1 > num2) {
        result = num1;
    }
    else {
        result = num2;
    }
}

max (3,5);

if ( (5!=5) or (2!=3) ) {
    q = 2323;
}

result = result + 10;

'''

from sly.lex import Token
from Lex import CalcLexer
from Yacc import CalcParser

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
