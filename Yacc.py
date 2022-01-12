
from sly import Parser
from Lex import CalcLexer  

class CalcParser(Parser):

    debugfile = 'parser.out'

    tokens = CalcLexer.tokens

    precedence = (
       ('left', OR),
       ('left', AND),
       ('left', BITWISE_AND),
       ('left', BITWISE_OR),
       ('left', LESS_THAN, LESS_THAN_EQ, GREATER_THAN, GREATER_THAN_EQ, IS_NOT_EQUAL, IS_EQUAL),
       ('left', PLUS, MINUS),
       ('left', DIVIDE, TIMES, MOD),
       ('right', UMINUS),
       ("right", EXPONENT),     
    )

    def __init__(self):
        self.allIDs = []
        self.variables = { }
        self.functions = { }

        self.local_func_names = None
        self.allIDs_local_var_inc = 0

    def error(self, p):

        if not p:
            print('Syntax error at the last line')
            return
        else:
            print('Syntax error around at the line #%r' %p.lineno)

    ############################## Grammar rules and actions ##############################

    #STATEMENT : ASSIGNMENT

    #STATEMENT : EXPRESSION

    #STATEMENT : LOOP

    #STATEMENT : CONDITIONAL

    #STATEMENT : FUNCTIONAL

    @_('STATEMENT SEMI_COL STATEMENT_LIST')
    def STATEMENT_LIST(self, production):
        return ('NODE_STATEMENT_LIST', production.STATEMENT, production.STATEMENT_LIST)

    @_('STATEMENT SEMI_COL')
    def STATEMENT_LIST(self, production):
        return ('NODE_STATEMENT_LIST', production.STATEMENT)

    @_('ASSIGNMENT')
    def STATEMENT(self, production):
        if not production.ASSIGNMENT[1] in self.allIDs:
            self.allIDs.append(production.ASSIGNMENT[1])
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

    @_('FUNCTIONAL')
    def STATEMENT(self, production):
        return ('NODE_STATEMENT', production.FUNCTIONAL) 

    ####################################################################################### 
     
    #ASSIGNMENT : ID = EXPRESSION
    @_('ID ASSIGN EXPRESSION')
    def ASSIGNMENT(self, production):
        return ('NODE_ASSIGNMENT', production.ID, production.EXPRESSION)
    
    #ASSIGNMENT : ID = EXPRESSION, ASSIGNMENT 
    @_("ID ASSIGN EXPRESSION COMMA ASSIGNMENT")
    def ASSIGNMENT(self, production):
        return ('NODE_ASSIGNMENT_EXP', production.ID, production.EXPRESSION, production.ASSIGNMENT)

    ########################################################################################## 

    @_('WHILE LPAREN EXPRESSION RPAREN LCURLY STATEMENT_LIST RCURLY')
    def LOOP(self, production):
        return ('NODE_WHILE', production.EXPRESSION, production.STATEMENT_LIST)

    ##########################################################################################

    #CONDITIONAL : IF ( BOOL_EXPRESSION ) { STATEMENT_LIST } 
    @_('IF LPAREN BOOL_EXPRESSION RPAREN LCURLY STATEMENT_LIST RCURLY')
    def CONDITIONAL(self, production):   
        return ("NODE_CONDITIONAL", production.BOOL_EXPRESSION, production.STATEMENT_LIST)

    #CONDITIONAL : IF ( BOOL_EXPRESSION ) { STATEMENT_LIST } ELSE { STATEMENT_LIST } 
    @_('IF LPAREN BOOL_EXPRESSION RPAREN LCURLY STATEMENT_LIST RCURLY ELSE LCURLY STATEMENT_LIST RCURLY')
    def CONDITIONAL(self, production):   
        return ("NODE_CONDITIONAL_ELSE", production.BOOL_EXPRESSION, production.STATEMENT_LIST0, production.STATEMENT_LIST1)

    #CONDITIONAL : IF ( BOOL_EXPRESSION ) { STATEMENT_LIST } ELSE CONDITIONAL 
    @_('IF LPAREN BOOL_EXPRESSION RPAREN LCURLY STATEMENT_LIST RCURLY ELSE CONDITIONAL')
    def CONDITIONAL(self, production):   
        return ("NODE_CONDITIONAL_ELSE_CONDITIONAL", production.BOOL_EXPRESSION, production.STATEMENT_LIST, production.CONDITIONAL)

    ##########################################################################################  

    #FUNCTION : FUNCTION_DEFINITION
    @_('FUNCTION_DEFINITION')
    def FUNCTIONAL(self, production):
        return ('NODE_FUNCTIONAL', production.FUNCTION_DEFINITION)

    #FUNCTION_DEFINITION : FUNCTION ID (PARAM_LIST) { STATEMENT_LIST }
    @_('FUNCTION ID LPAREN PARAM_LIST RPAREN LCURLY STATEMENT_LIST RCURLY')  
    def FUNCTION_DEFINITION(self, production):

        node = production.STATEMENT_LIST

        while(True):

            if(node[1][1][0] == 'NODE_ASSIGNMENT'):
                self.allIDs_local_var_inc += 1

            if(len(node) > 2):
                node = node[2]
            else:
                break

        for i in range(self.allIDs_local_var_inc):
            self.allIDs.pop()

        return ('NODE_FUNCTION_DEFINITION', production.ID, production.PARAM_LIST, production.STATEMENT_LIST)

    #PARAM_LIST : EMPTY
    @_('EMPTY')
    def PARAM_LIST(self, production):
        self.allIDs_lenght = len(self.allIDs)
        return None

    #PARAM_LIST : ID
    @_('ID')
    def PARAM_LIST(self, production):
        if not production.ID in self.allIDs:
            self.allIDs.append(production.ID)
            self.allIDs_local_var_inc += 1
        return (production.ID,)
    
    #PARAM_LIST : ID, PARAM_LIST
    @_('ID COMMA PARAM_LIST')
    def PARAM_LIST(self, production):
        if not production.ID in self.allIDs:
            self.allIDs.append(production.ID)
            self.allIDs_local_var_inc += 1
        return (production.ID, *production.PARAM_LIST)

    #############################################  
    
    #FUNCTION : FUNCTION_CALL
    @_('FUNCTION_CALL')
    def FUNCTIONAL(self, production):
        return ('NODE_FUNCTIONAL', production.FUNCTION_CALL)

    #FUNCTION_CALL : ID (VALUE_LIST)
    @_('ID LPAREN VALUE_LIST RPAREN')  
    def FUNCTION_CALL(self, production):
        return ('NODE_FUNCTION_CALL', production.ID, production.VALUE_LIST)

    #VALUE_LIST : EMPTY
    @_('EMPTY')
    def VALUE_LIST(self, production):
        return None

    #VALUE_LIST : EXPRESSION
    @_('EXPRESSION')
    def VALUE_LIST(self, production):
        return (production.EXPRESSION,)

    #VALUE_LIST : EXPRESSION, VALUE_LIST
    @_('EXPRESSION COMMA VALUE_LIST')
    def VALUE_LIST(self, production):
        return (production.EXPRESSION, *production.VALUE_LIST)

    ########################################################################################## 

    #EXPRESSION : NUMBER
    @_('NUMBER')
    def EXPRESSION(self, production):
        return ('NODE_NUMBER', production.NUMBER)

    #EXPRESSION : ID
    @_("ID")
    def EXPRESSION(self, production):
        if production.ID not in self.allIDs:
            print("Undefined Reference to " + production.ID + " at line " + str(production.lineno))
        return('NODE_ID', production.ID)

    #EXPRESSION : ( EXPRESSION )
    @_('LPAREN EXPRESSION RPAREN')
    def EXPRESSION(self, production):
        return ('NODE_LP_EXPRESSION_RP', production.EXPRESSION)

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

     #BOOL_EXPRESSION : ( BOOL_EXPRESSION )
    @_('LPAREN BOOL_EXPRESSION RPAREN')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_LP_BOOL_EXPRESSION_RP', production.BOOL_EXPRESSION)

    #BOOL_EXPRESSION : EXPRESSION == EXPRESSION
    @_('EXPRESSION IS_EQUAL EXPRESSION')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_IS_EQUAL', production.EXPRESSION0, production.EXPRESSION1)

    #BOOL_EXPRESSION : EXPRESSION != EXPRESSION
    @_('EXPRESSION IS_NOT_EQUAL EXPRESSION')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_IS_NOT_EQUAL', production.EXPRESSION0, production.EXPRESSION1)

    #BOOL_EXPRESSION : EXPRESSION >= EXPRESSION
    @_('EXPRESSION GREATER_THAN_EQ EXPRESSION')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_GREATER_THAN_EQ', production.EXPRESSION0, production.EXPRESSION1)

    #BOOL_EXPRESSION : EXPRESSION > EXPRESSION
    @_('EXPRESSION GREATER_THAN EXPRESSION')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_GREATER_THAN', production.EXPRESSION0, production.EXPRESSION1)

    #BOOL_EXPRESSION : EXPRESSION <= EXPRESSION
    @_('EXPRESSION LESS_THAN_EQ EXPRESSION')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_LESS_THAN_EQ', production.EXPRESSION0, production.EXPRESSION1)

    #BOOL_EXPRESSION : EXPRESSION < EXPRESSION
    @_('EXPRESSION LESS_THAN EXPRESSION')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_LESS_THAN', production.EXPRESSION0, production.EXPRESSION1)

    #######################################################################################

    #EXPRESSION : EXPRESSION & EXPRESSION
    @_('EXPRESSION BITWISE_AND EXPRESSION')
    def EXPRESSION(self, production):
        return ('NODE_BITWISE_AND', production.EXPRESSION0, production.EXPRESSION1)
    
    #EXPRESSION : EXPRESSION | EXPRESSION
    @_('EXPRESSION BITWISE_OR EXPRESSION')
    def EXPRESSION(self, production):
        return ('NODE_BITWISE_OR', production.EXPRESSION0, production.EXPRESSION1)

    #######################################################################################

    #BOOL_EXPRESSION : BOOL_EXPRESSION and BOOL_EXPRESSION
    @_('BOOL_EXPRESSION AND BOOL_EXPRESSION')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_AND', production.BOOL_EXPRESSION0, production.BOOL_EXPRESSION1)
    
    #BOOL_EXPRESSION : BOOL_EXPRESSION or BOOL_EXPRESSION
    @_('BOOL_EXPRESSION OR BOOL_EXPRESSION')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_OR', production.BOOL_EXPRESSION0, production.BOOL_EXPRESSION1)

    #######################################################################################

    @_('')
    def EMPTY(self, production):
        pass

    #######################################################################################

    def eval_ast(self, ast):

        if(ast == None):
            return

        #############################################

        elif(ast[0] == 'NODE_STATEMENT_LIST'):
            if(len(ast) > 2):
                return self.eval_ast(ast[1]), self.eval_ast(ast[2])
            else:
                return self.eval_ast(ast[1])

        elif(ast[0] == 'NODE_STATEMENT'):
            return self.eval_ast(ast[1])

        #############################################

        elif(ast[0] == 'NODE_ASSIGNMENT'):

            if(self.local_func_names == None):
                self.variables[ast[1]] = self.eval_ast(ast[2]) 
                return self.variables[ast[1]]
        
            else:
                #If There is a local variable
                if ast[1] in self.local_func_names:
                    self.local_func_names[ast[1]] = self.eval_ast(ast[2]) 
                    return self.local_func_names[ast[1]]
                #There was no local variable, check globals
                elif ast[1] in self.variables:
                    self.variables[ast[1]] = self.eval_ast(ast[2])
                    return self.variables[ast[1]]
                #There was no id so create one in local variables
                else:
                    self.local_func_names[ast[1]] = self.eval_ast(ast[2]) 
                    return self.local_func_names[ast[1]]

        elif(ast[0] == 'NODE_ASSIGNMENT_EXP'): 
            if(self.local_func_names == None):
                self.variables[ast[1]] = self.eval_ast(ast[2]) 
                return self.variables[ast[1]], self.eval_ast(ast[3]) 
        
            else:
                #If There is a local variable
                if ast[1] in self.local_func_names:
                    self.local_func_names[ast[1]] = self.eval_ast(ast[2]) 
                    return self.local_func_names[ast[1]], self.eval_ast(ast[3]) 
                #There was no local variable, check globals
                elif ast[1] in self.variables:
                    self.variables[ast[1]] = self.eval_ast(ast[2])
                    return self.variables[ast[1]], self.eval_ast(ast[3]) 
                #There was no id so create one in local variables
                else:
                    self.local_func_names[ast[1]] = self.eval_ast(ast[2]) 
                    return self.local_func_names[ast[1]], self.eval_ast(ast[3]) 
        
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

        elif(ast[0] == 'NODE_FUNCTIONAL'):
            return self.eval_ast(ast[1]) 

        elif(ast[0] == 'NODE_FUNCTION_DEFINITION'):

            param_dic = { } 

            if not ast[2]:
                self.functions[ast[1]] = (ast[1], ast[2], ast[3], param_dic)
                return

            for k in ast[2]:
                param_dic[k] = None

            self.functions[ast[1]] = (ast[1], ast[2], ast[3], param_dic)

            return 

        elif(ast[0] == 'NODE_FUNCTION_CALL'):

            foo = self.functions[ast[1]]

            if ast[2]:

                values = [ self.eval_ast(val) for val in ast[2] ]
                
                i = 0
                for k in foo[3]:
                    foo[3][k] = values[i]          
                    i += 1

            self.local_func_names = foo[3]
            f_result = self.eval_ast(foo[2])
            self.local_func_names = None

            return f_result

        #############################################

        elif(ast[0] == 'NODE_ID'):
            if(self.local_func_names == None):
                if ast[1] in self.variables:
                    return self.variables[ast[1]]
                else:
                    print("NO SUCH ID")
            else:
                if ast[1] in self.local_func_names:
                    return self.local_func_names[ast[1]]
                elif ast[1] in self.variables:
                    return self.variables[ast[1]]
                else:
                    print("NO SUCH ID")

        elif(ast[0] == 'NODE_NUMBER'):
            return ast[1]
   
        elif(ast[0] == 'NODE_LP_EXPRESSION_RP'):
            return self.eval_ast(ast[1])

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

        elif(ast[0] == 'NODE_LP_BOOL_EXPRESSION_RP'):
            return self.eval_ast(ast[1])

        elif(ast[0] == 'NODE_IS_EQUAL'):
            return self.eval_ast(ast[1]) == self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_IS_NOT_EQUAL'):
            return self.eval_ast(ast[1]) != self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_GREATER_THAN_EQ'):
            return self.eval_ast(ast[1]) >= self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_GREATER_THAN'):
            return self.eval_ast(ast[1]) > self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_LESS_THAN_EQ'):
            return self.eval_ast(ast[1]) <= self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_LESS_THAN'):
            return self.eval_ast(ast[1]) < self.eval_ast(ast[2])

        #############################################

        elif(ast[0] == 'NODE_BITWISE_AND'):
            return self.eval_ast(ast[1]) & self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_BITWISE_OR'):
            return self.eval_ast(ast[1]) | self.eval_ast(ast[2])
        
        #############################################

        elif(ast[0] == 'NODE_AND'):
            return True if (self.eval_ast(ast[1]) == True and self.eval_ast(ast[2]) == True) else False

        elif(ast[0] == 'NODE_OR'):
            return True if (self.eval_ast(ast[1]) == True or self.eval_ast(ast[2]) == True) else False

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

    #CONDITIONAL : IF error { STATEMENT_LIST } 
    @_('IF error SEMI_COL')
    def CONDITIONAL(self, production):   
        print("Invalid if block")

    #CONDITIONAL : IF error { STATEMENT_LIST } 
    @_('IF LPAREN error LCURLY STATEMENT_LIST RCURLY')
    def CONDITIONAL(self, production):   
        print("Missing ")

    #CONDITIONAL : IF ( error ) { STATEMENT_LIST } 
    @_('IF LPAREN error RPAREN LCURLY STATEMENT_LIST RCURLY')
    def CONDITIONAL(self, production):   
        print("Condition must be boolean")
