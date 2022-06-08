
%{
#include <stdio.h>
#include <string.h>
#include "parser.tab.h"
%}

%%

[ \t\n]                 ;
[a-zA-Z0-9]            return STRING;
[0-9]+                 return INT;
[a-zA-Z_][_a-zA-Z0-9]  return IDENTIFIER;


"="                     return EQUAL;
"pari"                  return IS_EQUAL;

"diverso"               return NOT;
"piu"                   return PLUS;
"meno"                  return MINUS;
"concatenare"           return CONCATENATE;

"moltiplicare"          return MULT;
"divedere"              return DIV;
"anche"                 return AND;
"oppure"                return OR;

"piu_grande"            return GREATER;
"piu_piccula"           return MINOR;
"loop"                  return WHILE;
"se_e"                    return IF;

"altro"                 return ELSE;
"dica"                  return PRINT;
"ricevere"              return SCANF;

"#$"                    return OPENPAR;
"$#"                    return CLOSEPAR;
";"                     return SEMI_COLON;
","                     return SEPARATOR;

"numero"               return VAR_TYPE;
"testo"                return VAR_TYPE;
"#ciao"                return OPEN_BLOCK;
"ciao#"                return CLOSE_BLOCK;
"return"               return RETURN;

.                       printf("Unknown token!n"); yyterminate();

%%