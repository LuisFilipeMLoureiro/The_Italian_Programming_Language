import sys
import re



class Node():   

    def __init__(self, value, ListOfNodes = []):
        self.value = value
        self.children = ListOfNodes

    def Evaluate(self, st):
        pass

class BinOp(Node):

    def Evaluate(self,st):

        cria1 = self.children[0].Evaluate(st)
        cria2 = self.children[1].Evaluate(st)

        if (cria1[1] == "int") and (cria2[1] == "int"):
            if self.value == "plus":
                
                result = cria1[0] + cria2[0]

            elif self.value == "minus":
                result  = cria1[0] - cria2[0]

            elif self.value == "mult":
                result  = cria1[0] * cria2[0]

            elif self.value == "div":
                result  = int(cria1[0] / cria2[0])

            elif self.value == "doubleEqual":
                result = (cria1[0] == cria2[0])

            elif self.value == "and":
                result = (cria1[0] and cria2[0])

            elif self.value == "above":
                result = (cria1[0] > cria2[0])

            elif self.value == "below":
                result = (cria1[0] < cria2[0])

            elif self.value == "or":
                result = (cria1[0] or cria2[0])

            elif self.value == "concat":
                result = str(cria1[0]) + str(cria2[0])
                return (str(result), "str")
            else:
                sys.stderr.write("Invalid operation with integer in BinOp!")
                raise ValueError

            return (int(result), "int")

        elif (cria1[1] == "str") and (cria2[1] == "str"):
            if self.value == "concat":
                result = str(cria1[0]) + str(cria2[0])
                return (str(result), "str")

            if self.value == "doubleEqual":
                result = str(cria1[0]) == str(cria2[0])
                return (int(result), "int")
            elif self.value == "above":
                result = (str(cria1[0]) > str(cria2[0]))
                return (int(result), "int")
            elif self.value == "below":
                result = (str(cria1[0]) < str(cria2[0]))
                return (int(result), "int")

            else:
                sys.stderr.write("Invalid operation with string in BinOp!")
                raise ValueError
        
        elif (cria1[1] == "str") or (cria2[1] == "str"):
            if self.value == "concat":
                result = str(cria1[0]) + str(cria2[0])
                return (str(result), "str")

            else:
                sys.stderr.write("Invalid operation with string and int in BinOp!")
                raise ValueError



class UnOp(Node):
    def Evaluate(self, st):
        result = self.children[0].Evaluate(st)

         
        if result[1] == "int":
            if self.value == "minus":
                output = result[0] * -1
            elif self.value == "plus":
                output = result[0]
            elif self.value == "not":
                output = not(result[0])
        else:
            sys.stderr.write("Must be a int to be operated!")
            raise ValueError




        return (int(output), "int")

class WHILE(Node):
    def Evaluate(self, st):
        while self.children[0].Evaluate(st)[0]:
            self.children[1].Evaluate(st)

class SCANF(Node):
    def Evaluate(self, st):
        resultado =  int(input())
        return [resultado, "int"]

class IF(Node):
    def Evaluate(self, st):
        if self.children[0].Evaluate(st):
            self.children[1].Evaluate(st)
            

        elif len(self.children) > 2:
            self.children[2].Evaluate(st)


class Block(Node):
    def Evaluate(self, st):
        for n in self.children:
            n.Evaluate(st)

class IntVal(Node):
    def Evaluate(self, st):
        return (self.value, "int")

class NoOp(Node):
    def Evaluate(self, st):
        pass



dic_FuncTable = {}
class FuncTable:

    @staticmethod
    def create(nome, value, tipo): 
        if nome in dic_FuncTable:
            sys.stderr.write("Invalid casting or more than one declaration of a function")
            raise ValueError 
        else:
            dic_FuncTable[nome] = [value, tipo]
        
        

    @staticmethod
    def getter(chave):
        return dic_FuncTable[chave]



class SymbolTable:
    def __init__(self):
        self.SymbolTable = {}
    
    def create(self,nome, tipo):
        if nome in self.SymbolTable.keys():
            sys.stderr.write("Invalid casting or more than one declaration of a variable")
            raise ValueError 
        else:
            self.SymbolTable[nome] = [None, tipo]
   
    def getter(self,chave):
        return  self.SymbolTable[chave]       

    def setter(self,nome, valor):
        if nome in self.SymbolTable.keys():
            if valor[1] == self.SymbolTable[nome][1]:
                self.SymbolTable[nome] = [valor[0], valor[1]]

            else:
                sys.stderr.write("Invalid association")
                raise ValueError 
        else:
            sys.stderr.write("Variable not declared")
            raise ValueError 



class FuncDec(Node):
    def Evaluate(self, st):
        vardec = self.children[0]
        neto = vardec.children
        
        FuncTable.create(neto.value, self, vardec.value)


class FuncCall(Node):
    def Evaluate(self, st):
        funcName = self.value
        funcdec, tipo = FuncTable.getter(funcName)
        current_st = SymbolTable() 

        if (len(funcdec.children)-2) == len(self.children): 
            for i in range(1,len(funcdec.children)-1):
                vardec = self.children[i].value
                neto = vardec.children[i].value
                                
                current_st.create(neto, vardec)

            #variaveis locais da funcao
            for child in self.children:                
                current_st.setter(neto.value, child.Evaluate(st))
                
            nodeBlock = funcdec.children[-1].Evaluate(st)
            
            return nodeBlock
                

                
            
        
        else:
            sys.stderr.write("Inconsistent number of arguments in function")
            raise ValueError      

            
            
class ReturnNode(Node):
    def Evaluate(self, st):
        
        return self.children.Evaluate(st)
        


class Assignment(Node):
    def Evaluate(self, st):
        cria1 = self.children[0]
        cria2 = self.children[1].Evaluate(st)
        

        st.setter(cria1, cria2)

class Printf(Node):
    def Evaluate(self, st):
        cria1 = self.children.Evaluate(st)
        print(cria1[0])

class Identifier(Node):
    def Evaluate(self, st):
        variavel = st.getter(self.value)
        return(variavel[0],variavel[1])

class Strval(Node):
    def Evaluate(self, st):
        return(self.value, "str")

class Vardec(Node):
    def Evaluate(self, st):
        _value = self.value
        for ident in self.children:
            st.create(ident.value, _value)

            
        


#https://stackoverflow.com/questions/241327/remove-c-and-c-comments-using-python
class PrePro:
    @staticmethod
    def filter(arg):
        new_arg = re.sub(r"\/\*.*?\*\/", "", arg)
        return new_arg

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Tokenizer:
    def __init__(self,origin):
        self.origin = origin #codigo fonte
        self.position = 0 #posição inicial é 0
        self.actual = self.origin[0] #inicio no primeiro token


    
    def selectNext(self):
        
    
        numero = ""
        numbers = ["1", "2", "3", "4", "5", "6","7", "8","9","0"]
        ReservedWords = ["dica", "ricevere", "se", "loop", "altro", "int", "str", "return", "void", "piu", "meno", "diverso", "moltiplicare", "divedere", "anche", "oppure", "piu_grande", "piu_piccula", "pari"]
        

        while(self.position <= len(self.origin) - 1):
            i = self.origin[self.position]

            if i in numbers:
                                
                numero += i 
                                         
            elif (numero != ""):                
                self.actual = Token("int",int(numero))       
                numero = ""
                return self.actual
           
            if(self.position == len(self.origin) - 1) & (i in numero):               
                self.actual = Token("int",int(numero))               
                self.position +=1                 
                return self.actual
            
            if i == "(":
                self.actual = Token("open_p", "(")
                self.position +=1
                return self.actual
            
            if i == ")":
                self.actual = Token("close_p", ")")
                self.position +=1
                return self.actual

            if i == "$":
                self.actual = Token("END", ";")
                self.position +=1
                return self.actual
            if i == "{":
                self.actual = Token("open_block", "{")
                self.position +=1
                return self.actual
            
            if i == "}":
                self.actual = Token("close_block", "}")
                self.position +=1
                return self.actual

            if i == ".":
                self.actual = Token("concat", ".")
                self.position +=1
                return self.actual
            if i == ",":
                self.actual = Token("comma", ",")
                self.position +=1
                return self.actual

            if i == "=":                
                self.actual = Token("equal", "=") 
                self.position +=1
                return self.actual

            

            variavel = ""
            if "\"" == i:
                self.position += 1
                while self.origin[self.position] != ("\""):
                    variavel += self.origin[self.position]
                    self.position += 1
                
                self.position += 1
                self.actual = Token("str",variavel)
                return self.actual

            if(self.origin[self.position].isalpha()):          
                while(self.position < len(self.origin)-1) and (self.origin[self.position].isnumeric() or self.origin[self.position].isalpha() or self.origin[self.position] == "_" ):
                    variavel += self.origin[self.position]
                    self.position += 1
                if variavel in ReservedWords:
                    if variavel == "str":
                        self.actual = Token("type","str")
                    elif variavel == "int":
                        self.actual = Token("type","int")
                    elif variavel == "void":
                        self.actual = Token("type","void")
                    elif variavel == "piu":
                         self.actual = Token("plus", "piu")
                    elif variavel == "dica":
                        self.actual = Token("printf", "dica")
                    elif variavel == "meno":
                        self.actual = Token("minus", "meno")
                    elif variavel == "diverso":
                        self.actual = Token("not", "diverso")
                    elif variavel == "moltiplicare":
                        self.actual = Token("mult", "moltiplicare")
                    elif variavel == "anche":
                        self.actual = Token("and", "anche")
                    elif variavel == "oppure":
                        self.actual = Token("or", "oppure")
                    elif variavel == "divedere":
                        self.actual = Token("div", "divedere")
                    elif variavel == "piu_grande":
                        self.actual = Token("above", "piu_grande")
                    elif variavel == "piu_piccula":
                        self.actual = Token("below", "piu_piccula")
                    elif variavel == "pari":
                        self.actual = Token("doubleEqual", "pari")
                    elif variavel == "loop":
                        self.actual = Token("while", "loop")
                    elif variavel == "se":
                        self.actual = Token("if", "se")
                    elif variavel == "altro":
                        self.actual = Token("else", "altro")
                    elif variavel == "ricevere":
                        self.actual = Token("scanf", "ricevere")



                    else:
                        self.actual = Token(variavel,variavel)
                    
                else:
                    self.actual = Token("ID",variavel)
            
                return self.actual
            



            
            self.position +=1 
                     
                     
                
        self.actual = Token("EOF", "")
        

        return self.actual
        

class Parser:


    @staticmethod
    def parseDeclaration():
        
        if(Parser.token.actual.type == "type"):
            filhos = []
            funcType = Parser.token.actual.value
            Parser.token.selectNext()
            if(Parser.token.actual.type == "ID"):
                funcID = Parser.token.actual.value
                arg0 = (Vardec(funcType, Identifier(funcID)))
                filhos.append(arg0)
                Parser.token.selectNext()

                if(Parser.token.actual.type == "open_p"):
                    Parser.token.selectNext()

                    if(Parser.token.actual.type == "close_p"):
                        Parser.token.selectNext()                                                
                        filhos.append(Parser.parseBlock())
                        result = FuncDec(funcID, filhos)
                        return result
                    

                    if(Parser.token.actual.type == "type"):
                        typevar = Parser.token.actual.value
                        Parser.token.selectNext() 
                                     
                                                            
                        if(Parser.token.actual.type == "ID"):
                            nomevar = Parser.token.actual.value
                            filhos.append(Vardec(typevar, Identifier(nomevar)))
                            Parser.token.selectNext()                                   
                            while (Parser.token.actual.type == "comma"):
                                Parser.token.selectNext() 
                                
                                if (Parser.token.actual.type == "type"):
                                    typevar = Parser.token.actual.value
                                    Parser.token.selectNext()
                                    
                                    if (Parser.token.actual.type == "ID"):
                                        nomevar = Parser.token.actual.value
                                        Parser.token.selectNext()
                                        filhos.append(Vardec(typevar, Identifier(nomevar)))

                                    else:
                                        sys.stderr.write("Missing name of argument")
                                        raise ValueError

                                else:
                                    sys.stderr.write("Missing type in argument")
                                    raise ValueError


                            if(Parser.token.actual.type == "close_p"):
                                    filhos.append(Parser.parseBlock())
                                    result = FuncDec(funcID, filhos)
                                    return result 
                                
                            else:
                                sys.stderr.write("Missing closing parentheses in function declaration")
                                raise ValueError
                 
            else:
                sys.stderr.write("Missing function name")
                raise ValueError 
        else:
            sys.stderr.write("Missing a function at the start")
            raise ValueError 
        

    
    @staticmethod
    def parseProgram(): 
        nodes = []
        while(Parser.token.actual.type != "EOF"):
            
            nodes.append(Parser.parseDeclaration())

        
            
        return Block("Block", nodes)

    @staticmethod 
    def parseBlock():
        nodes = []
        if (Parser.token.actual.type != "open_block"):
            sys.stderr.write("Missing opening block {")
            raise ValueError 

        Parser.token.selectNext()
        while(Parser.token.actual.type != "close_block"):    
            result = Parser.parseStatement()
            nodes.append(result)

        Parser.token.selectNext()
        return Block("", nodes)


    @staticmethod
    def parseStatement():       
        

        if(Parser.token.actual.type == "END"):
            Parser.token.selectNext()
            node = NoOp(None)
            return node

        #Parser.token.selectNext()
        if(Parser.token.actual.type == "ID"):
            result = Parser.token.actual.value
            argumentos = []
            Parser.token.selectNext()
            if(Parser.token.actual.type == "open_p"):
                Parser.token.selectNext()
                argumentos.append(Parser.parseRelExpression())
                Parser.token.selectNext()
                
                while(Parser.token.actual.type == "comma"):
                    Parser.token.selectNext() 
                    argumentos.append(Parser.parseRelExpression())

                if(Parser.token.actual.type == "close_p"):
                    Parser.token.selectNext()
                    return FuncCall(result, argumentos)
                else:
                    sys.stderr.write("Missing opening parenteses in statement")
                    raise ValueError 


            elif(Parser.token.actual.type == "equal"):
                
                Parser.token.selectNext()

                node =  Assignment("equal", [result, Parser.parseRelExpression()]) 

                if(Parser.token.actual.type == "END"):
                    Parser.token.selectNext()
                    return node
                else: 
                    sys.stderr.write("Missing closing token ;")
                    raise ValueError  

            else:
                sys.stderr.write("Missing =")
                raise ValueError
        

        
        elif(Parser.token.actual.type == "printf"):

            Parser.token.selectNext()

            if(Parser.token.actual.type == "open_p"):
                Parser.token.selectNext()
                result = Parser.parseRelExpression()
                if(Parser.token.actual.type == "close_p"):
                    node = Printf("printf", result) 
                    Parser.token.selectNext()
                    
                    if(Parser.token.actual.type == "END"):
                        Parser.token.selectNext()
                        return node
                    else:
                        sys.stderr.write("Missing closing statement ;")
                        raise ValueError                   
                else:
                    sys.stderr.write("Missing closing parenteses")
                    raise ValueError
            else:
                sys.stderr.write("Missing opening parenteses")
                raise ValueError

        
        elif(Parser.token.actual.type == "type"):
            if (Parser.token.actual.value) == "int":
                result = Vardec("int", [])
                
            elif(Parser.token.actual.value) == "str":
                result = Vardec("str", [])                
            
            Parser.token.selectNext()
            if Parser.token.actual.type == "ID":            
                variavel = Parser.token.actual.value
               
                result.children.append(Identifier(variavel))
                Parser.token.selectNext()
            else:
                sys.stderr.write("Missing name of variable in declaration")
                raise ValueError           

            while Parser.token.actual.type == "comma":
                Parser.token.selectNext()
                if Parser.token.actual.type == "ID":  
                    variavel = Parser.token.actual.value
                    result.children.append(Identifier(variavel))
                    Parser.token.selectNext()
                else:
                    sys.stderr.write("Missing name of variable in list of declarations")
                    raise ValueError           
            
            
            
            if(Parser.token.actual.type != "END"):
                sys.stderr.write("Missing ; in declaration of variable")
                raise ValueError            
            else:
                return result

        elif(Parser.token.actual.type == "return"):
            Parser.token.selectNext()
            if(Parser.token.actual.type == "open_p"):
                Parser.token.selectNext()
                result = Parser.parseRelExpression()
                if(Parser.token.actual.type == "close_p"):
                    Parser.token.selectNext()
                    if(Parser.token.actual.type == "END"):

                        return ReturnNode("return", result)
                    else:
                        sys.stderr.write("Missing ; in return")
                        raise ValueError


                else:
                    sys.stderr.write("Missing closing parenteses in return")
                    raise ValueError

        
        elif(Parser.token.actual.type == "while"):
            Parser.token.selectNext()
            if(Parser.token.actual.type == "open_p"):
                Parser.token.selectNext()
                result = Parser.parseRelExpression()                
                
                if(Parser.token.actual.type == "close_p"):
                    Parser.token.selectNext()                  
                    result2 = Parser.parseStatement()
                    node = WHILE("", [result, result2])
                    return node                   

                else:
                    sys.stderr.write("Missing closing parenteses in while")
                    raise ValueError
            else:
                sys.stderr.write("Missing opening parenteses in while")
                raise ValueError

        elif(Parser.token.actual.type == "if"):
            Parser.token.selectNext()
            if(Parser.token.actual.type == "open_p"):
                Parser.token.selectNext()
                result = Parser.parseRelExpression()

                if(Parser.token.actual.type == "close_p"):
                    Parser.token.selectNext()
                    result2 = Parser.parseStatement()      

                    if(Parser.token.actual.type == "else"):
                        Parser.token.selectNext()
                        result3 = Parser.parseStatement()
                        node = IF("",[result, result2, result3])
                        return node
                        
                    else:                        
                        node = IF("",[result, result2])
                        return node
                else:
                    sys.stderr.write("Missing opening parenteses in if")
                    raise ValueError
            else:
                sys.stderr.write("Missing opening parenteses in if")
                raise ValueError
        
        else:
            node = Parser.parseBlock()
            return node

    @staticmethod
    def parseRelExpression():

        result = Parser.parseExpression()

        while(Parser.token.actual.type == "doubleEqual" or Parser.token.actual.type == "above" or Parser.token.actual.type == "below"):   
            
            if(Parser.token.actual.type == "doubleEqual"):
                Parser.token.selectNext()
                result = BinOp("doubleEqual", [result, Parser.parseExpression()]) 

            if(Parser.token.actual.type == "above"):
                Parser.token.selectNext()
                result = BinOp("above", [result, Parser.parseExpression()]) 

            if(Parser.token.actual.type == "below"):
                Parser.token.selectNext()
                result = BinOp("below", [result, Parser.parseExpression()]) 

        return result
        

    @staticmethod
    def parseExpression():
        
        result = Parser.parseTerm()


        while(Parser.token.actual.type == "plus" or Parser.token.actual.type == "minus" or Parser.token.actual.type == "or" or Parser.token.actual.type == "concat" ):       

            if(Parser.token.actual.type == "plus"): 
                Parser.token.selectNext()                   
                result = BinOp("plus", [result, Parser.parseTerm()])                
                           
                               
            if(Parser.token.actual.type == "minus"):
                Parser.token.selectNext()
                result = BinOp("minus", [result, Parser.parseTerm()])

            if(Parser.token.actual.type == "or"):
                Parser.token.selectNext()
                result = BinOp("or", [result, Parser.parseTerm()])
            if(Parser.token.actual.type == "concat"):
                Parser.token.selectNext()
                result = BinOp("concat", [result, Parser.parseTerm()])  

            
            
        return result
        




    @staticmethod
    def parseTerm():       
        
        result = Parser.parseFactor()    
    
        if (type(result) == int) & (Parser.token.actual.type == "int"):
            sys.stderr.write("Faltou operador")
            raise ValueError


        while(Parser.token.actual.type == "mult" or Parser.token.actual.type == "div" or Parser.token.actual.type == "and"):
            if(Parser.token.actual.type == "mult"):
                Parser.token.selectNext()
                result = BinOp("mult", [result, Parser.parseFactor()])
                               
                                               

            elif(Parser.token.actual.type == "div"):   
                Parser.token.selectNext()
                result = BinOp("div", [result, Parser.parseFactor()])


            elif(Parser.token.actual.type == "and"):   
                Parser.token.selectNext()
                result = BinOp("and", [result, Parser.parseFactor()])
                    

            #Parser.token.selectNext()
        return result

    @staticmethod
    def parseFactor():
        

        if(Parser.token.actual.type == "int"):
            number = int(Parser.token.actual.value) 
            result = IntVal(number)
            Parser.token.selectNext()
            return result

        elif(Parser.token.actual.type == "str"):
            number = Parser.token.actual.value
            result = Strval(number)
            Parser.token.selectNext()
            return result

              
        elif(Parser.token.actual.type == "ID"):
            result = Parser.token.actual.value
            Parser.token.selectNext()

            if(Parser.token.actual.type == "open_p"):
                Parser.token.selectNext()
                argumentos = []
                if(Parser.token.actual.type == "close_p"):
                    Parser.token.selectNext()
                    return FuncCall(result, argumentos)
                else:
                
                    argumentos.append(Parser.parseRelExpression())
                while(Parser.token.actual.type == "comma"):
                    Parser.token.selectNext()
                    argumentos.append(Parser.parseRelExpression())
                if(Parser.token.actual.type == "close_p"):
                    return FuncCall(result, argumentos)
                else:
                    sys.stderr.write("Missing opening parenteses in factor")
                    raise ValueError               
            
            else:           

                return Identifier(result)

        elif(Parser.token.actual.type == "plus"):
            Parser.token.selectNext()
            return UnOp("plus", [Parser.parseFactor()]) ### Recursion

        elif(Parser.token.actual.type == "minus"):
            Parser.token.selectNext() 
            return UnOp("minus", [Parser.parseFactor()]) ### Recursion

        elif(Parser.token.actual.type == "not"):
            Parser.token.selectNext() 
            return UnOp("not", [Parser.parseFactor()]) ### Recursion

        elif(Parser.token.actual.type == "open_p"):
            Parser.token.selectNext()
            result = Parser.parseRelExpression()
            if(Parser.token.actual.type == "close_p"):
                Parser.token.selectNext()
                return result
            else:
                sys.stderr.write("Sequencia invalida de parenteses")
                raise ValueError


        elif(Parser.token.actual.type == "scanf"):
            Parser.token.selectNext()
            if(Parser.token.actual.type == "open_p"):
                node = SCANF(Node)
                Parser.token.selectNext()
                if(Parser.token.actual.type == "close_p"):
                    Parser.token.selectNext()
                    return node
                else:
                    sys.stderr.write("Missing closing parenteses in scanf")
                    raise ValueError                

            else:
                sys.stderr.write("Missing opening parenteses in scanf")
                raise ValueError
        else:

            sys.stderr.write("Token invalido na posicao")
            raise ValueError
  
    
    @staticmethod
    def run(codigo_fonte):
        codigo_base = PrePro.filter(codigo_fonte)
        Parser.token = Tokenizer(codigo_base)
        Parser.token.selectNext() 
         
        
        result = Parser.parseProgram() #result é a arvore de nodes
        result.children.append(FuncCall("main",[]))


        if Parser.token.actual.type != "EOF":
            sys.stderr.write("Codigo fonte não foi inteiro consumido!")
            raise ValueError
            
 
        else:
            
            return result
          


entrada = sys.argv[1]

if ".c" in entrada:
    with open(entrada, "r") as file:
        result = Parser.run(file.read())
        temp_st = SymbolTable()
        result.Evaluate(temp_st)

        
else:
    sys.stderr.write("Must be a .c file !")
    raise ValueError








