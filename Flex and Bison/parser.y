%{
  #include<stdio.h>
  int yylex();
  void yyerror(const char *s) { printf("ERROR: %sn", s); }
%}

%token IDENTIFIER INT STRING
%token EQUAL IS_EQUAL MINOR GREATER NOT AND OR
%token OPENPAR CLOSEPAR OPEN_BLOCK CLOSE_BLOCK SEMI_COLON
%token PRINT SCANF WHILE IF ELSE VAR_TYPE RETURN
%token CONCATENATE SEPARATOR PLUS MINUS MULT DIV

%start program

%%

program : block 
        ;

block : OPEN_BLOCK statement CLOSE_BLOCK
      | OPEN_BLOCK CLOSE_BLOCK
      ;
        
statement : assigment
          | block
          | print
          | if
          | while
          | var_type
          SEMI_COLON
          ;
        
relexpression: expression IS_EQUAL expression
             | expression MINOR expression
             | expression GREATER expression
             | expression
             ;

expression: term PLUS term
          | term MINUS term
          | term OR term
          | term CONCATENATE term
          | term
          ;

term: factor
    | factor MULT factor
    | factor DIV factor
    | factor AND factor
    ;

factor: INT
    | STRING
    | IDENTIFIER
    | PLUS factor
    | MINUS factor
    | NOT factor
    | SCANF OPENPAR CLOSEPAR
    | OPENPAR relexpression CLOSEPAR
    ;

assigment: var_type IDENTIFIER EQUAL relexpression;
print: PRINT OPENPAR relexpression CLOSEPAR;
if: IF OPENPAR relexpression CLOSEPAR statement else;
while: WHILE OPENPAR relexpression CLOSEPAR statement;
else: ELSE statement;
var_type: VAR_TYPE IDENTIFIER
        | SEPARATOR IDENTIFIER
        ;

%%

int main(){
  yyparse();
  return 0;
}
