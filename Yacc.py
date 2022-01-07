from sly import Parser
from Lex import CalcLexer  

class CalcParser(Parser):

    debugfile = 'parser.out'

    tokens = CalcLexer.tokens

    precedence = (
       ('left', IS_EQUAL, IS_NOT_EQUAL),
       ('left', PLUS, MINUS),
       ('left', DIVIDE, TIMES, MOD),
       ('right', UMINUS),
       ("right", EXPONENT),     
    )

    def __init__(self):
        self.names = { }
        self.functions = { }

    ############################## Grammar rules and actions ##############################

    #STATEMENT : ASSIGNMENT

    #STATEMENT : EXPRESSION

    #STATEMENT : LOOP

    #STATEMENT : CONDITIONAL

    #STATEMENT : FUNCTION

    @_('ASSIGNMENT')
    def STATEMENT(self, production):
        return ('NODE_STATEMENT', production.ASSIGNMENT)

    @_('EXPRESSION')
    def STATEMENT(self, production):
        return ('NODE_STATEMENT', production.EXPRESSION)

    @_('LOOP')
    def STATEMENT(self, production):
        return ('NODE_STATEMENT', production.LOOP) 

    @_('CONDITIONAL')
    def STATEMENT(self, production):
        return ('NODE_STATEMENT', production.CONDITIONAL) 

    @_('FUNCTION')
    def STATEMENT(self, production):
        return ('NODE_STATEMENT', production.FUNCTION) 

    ####################################################################################### 
     
    #ASSIGNMENT : ID = EXPRESSION
    @_('ID ASSIGN EXPRESSION')
    def ASSIGNMENT(self, production):
        return ('NODE_ASSIGNMENT', production.ID, production.EXPRESSION)
    
    #ASSIGNMENT : ID = EXPRESSION, ASSIGNMENT <-------- new line
    @_("ID ASSIGN EXPRESSION COMMA ASSIGNMENT")
    def ASSIGNMENT(self, production):
        return ('NODE_ASSIGNMENT_EXP', production.ID, production.EXPRESSION, production.ASSIGNMENT)

    ########################################################################################## 

    @_("WHILE LPAREN EXPRESSION RPAREN LCURLY STATEMENT RCURLY")
    def LOOP(self, production):
        return ('NODE_WHILE', production.EXPRESSION, production.STATEMENT)

    ##########################################################################################

    #CONDITIONAL : IF ( EXPRESSION ) { STATEMENT } 
    @_('IF LPAREN EXPRESSION RPAREN LCURLY STATEMENT RCURLY')
    def CONDITIONAL(self, production):   
        return ("NODE_CONDITIONAL", production.EXPRESSION, production.STATEMENT)
        
    #CONDITIONAL : IF ( EXPRESSION ) { STATEMENT } ELSE { STATEMENT } 
    @_('IF LPAREN EXPRESSION RPAREN LCURLY STATEMENT RCURLY ELSE LCURLY STATEMENT RCURLY')
    def CONDITIONAL(self, production):   
        return ("NODE_CONDITIONAL_ELSE", production.EXPRESSION, production.STATEMENT0, production.STATEMENT1)

    #CONDITIONAL : IF ( EXPRESSION ) { STATEMENT } ELSE CONDITIONAL 
    @_('IF LPAREN EXPRESSION RPAREN LCURLY STATEMENT RCURLY ELSE CONDITIONAL')
    def CONDITIONAL(self, production):   
        return ("NODE_CONDITIONAL_ELSE_CONDITIONAL", production.EXPRESSION, production.STATEMENT, production.CONDITIONAL)

    ##########################################################################################  

    #FUNCTION : FUNCTION_DEFINITION

    #FUNCTION : FUNCTION_CALL

    @_('FUNCTION ID LPAREN PARAM_LIST RPAREN LCURLY STATEMENT RCURLY')  
    def FUNCTION_DEFINITON(self, production):
        return

    @_('ID LPAREN PARAM_LIST RPAREN')  
    def FUNCTION_DEFINITON(self, production):
        return

    ########################################################################################## 

    #EXPRESSION : NUMBER
    @_('NUMBER')
    def EXPRESSION(self, production):
        return ('NODE_NUMBER', production.NUMBER)

    #EXPRESSION : ID
    @_("ID")
    def EXPRESSION(self, production):
        return('NODE_ID', production.ID)

    #EXPRESSION : ( EXPRESSION )
    @_('LPAREN EXPRESSION RPAREN')
    def EXPRESSION(self, production):
        return ('NODE_LP_EXPRESSION_RP', production.LPAREN, production.EXPRESSION, production.RPAREN)

    #EXPRESSION : -EXPRESSION 
    @_('MINUS EXPRESSION %prec UMINUS')
    def EXPRESSION(self, production):
        return ('NODE_UMINUS', production.EXPRESSION)

    #EXPRESSION : EXPRESSION + EXPRESSION
    @_("EXPRESSION PLUS EXPRESSION")
    def EXPRESSION(self, production):
        return ('NODE_PLUS', production.EXPRESSION0, production.EXPRESSION1)

    #EXPRESSION : EXPRESSION - EXPRESSION
    @_("EXPRESSION MINUS EXPRESSION")
    def EXPRESSION(self, production):
        return ('NODE_MINUS', production.EXPRESSION0, production.EXPRESSION1)

    #EXPRESSION : EXPRESSION * EXPRESSION   
    @_("EXPRESSION TIMES EXPRESSION")
    def EXPRESSION(self, production):
        return ('NODE_TIMES', production.EXPRESSION0, production.EXPRESSION1)

    #EXPRESSION : EXPRESSION / EXPRESSION   
    @_("EXPRESSION DIVIDE EXPRESSION")
    def EXPRESSION(self, production):
        return ('NODE_DIVIDE', production.EXPRESSION0, production.EXPRESSION1)
    
    #EXPRESSION : EXPRESSION % EXPRESSION
    @_('EXPRESSION MOD EXPRESSION')
    def EXPRESSION(self, production):
        return ('NODE_MOD', production.EXPRESSION0, production.EXPRESSION1)

    #EXPRESSION : EXPRESSION ** EXPRESSION
    @_('EXPRESSION EXPONENT EXPRESSION')
    def EXPRESSION(self, production):
        return ('NODE_EXPONENT', production.EXPRESSION0, production.EXPRESSION1)  
    
    ##########################################################################################  

    #EXPRESSION : EXPRESSION == EXPRESSION
    @_('EXPRESSION IS_EQUAL EXPRESSION')
    def EXPRESSION(self, production):
        return ('NODE_IS_EQUAL', production.EXPRESSION0, production.EXPRESSION1)

    @_('EXPRESSION IS_NOT_EQUAL EXPRESSION')
    def EXPRESSION(self, production):
        return ('NODE_IS_NOT_EQUAL', production.EXPRESSION0, production.EXPRESSION1)

    #######################################################################################

    def eval_ast(self, ast):

        if(ast == None):
            return

        #############################################

        elif(ast[0] == 'NODE_STATEMENT'):
            return self.eval_ast(ast[1])

        #############################################

        elif(ast[0] == 'NODE_ASSIGNMENT'):
            try:
                self.names[ast[1]] = self.eval_ast(ast[2])      
                return self.names[ast[1]]
            except LookupError:
                print(f'Undefined name {ast[1]!r}')

        elif(ast[0] == 'NODE_ASSIGNMENT_EXP'): # <----------- New Line
            try:
                self.names[ast[1]] = self.eval_ast(ast[2])     
                return self.names[ast[1]] , self.eval_ast(ast[3])
            except LookupError:
                print(f'Undefined name {ast[1]!r}')
        
        #############################################

        elif(ast[0] == 'NODE_CONDITIONAL'):
            return self.eval_ast(ast[2]) if (self.eval_ast(ast[1]) == True) else None

        elif(ast[0] == 'NODE_CONDITIONAL_ELSE'):
            return self.eval_ast(ast[2]) if (self.eval_ast(ast[1]) == True) else self.eval_ast(ast[3])

        elif(ast[0] == 'NODE_CONDITIONAL_ELSE_CONDITIONAL'):
            return self.eval_ast(ast[2]) if (self.eval_ast(ast[1]) == True) else self.eval_ast(ast[3])
        
        #############################################

        elif(ast[0] == 'NODE_WHILE'):
            loop_result = None

            while( self.eval_ast(ast[1]) == True ):
                loop_result = self.eval_ast(ast[2]) 
  
            return loop_result
           
        #############################################

        elif(ast[0] == 'NODE_ID'):
            return self.names[ast[1]]

        elif(ast[0] == 'NODE_NUMBER'):
            return ast[1]
   
        elif(ast[0] == 'NODE_LP_EXPRESSION_RP'):
            return self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_UMINUS'):
            return -self.eval_ast(ast[1])

        elif(ast[0] == 'NODE_PLUS'):
            return self.eval_ast(ast[1]) + self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_MINUS'):
            return self.eval_ast(ast[1]) - self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_TIMES'):
            return self.eval_ast(ast[1]) * self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_DIVIDE'):
            return self.eval_ast(ast[1]) / self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_MOD'):
            return self.eval_ast(ast[1]) % self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_EXPONENT'):
            return self.eval_ast(ast[1]) ** self.eval_ast(ast[2])

        #############################################

        elif(ast[0] == 'NODE_IS_EQUAL'):
            return self.eval_ast(ast[1]) == self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_IS_NOT_EQUAL'):
            return self.eval_ast(ast[1]) != self.eval_ast(ast[2])

    #######################################################################################

    def parse(self, tokens):
        result = super(CalcParser, self).parse(tokens)

        x = None

        if type(result) == tuple:
            x = self.eval_ast(result)
        else:
            x = result

        print(x)

        return x

    #######################################################################################
    