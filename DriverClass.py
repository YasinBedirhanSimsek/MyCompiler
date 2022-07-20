from sly.lex import Token
from Lex import CalcLexer
from Yacc import CalcParser

if __name__ == '__main__':
                 
    lexer  = CalcLexer()
    parser = CalcParser()

    lines = None

    #f_path = 'declarationinitializationOfVariables.txt'
    #f_path = 'unreferencedIdentifierError.txt'
    #f_path = 'localVariablevsGlobal.txt'
    #f_path = 'simpleConditionalBlock.txt'
    #f_path = 'combinedLogic.txt'
    #f_path = 'whileLoopWithBreak.txt'
    #f_path = 'functionalStatment.txt'
    
    #with open(f_path) as f:
    #    lines = f.read()

    lines = 'a = 4;'

    while True:
        try:
            result = parser.parse(lexer.tokenize(lines))
            break
        except Exception as e:
            print(e)
            break
