grammar LXScript;

// Lexer

NUMBER
    : [0-9]+
    ;

NAME
    : [\w_]+
    ;

ID
    : NAME NUMBER?
    | NUMBER
    ;

// Sigils for different types of IDs
BANG    : '!'; // Setting
DOLLARS : '$'; // Sequence

// Comments and whitespace
POUND : '#';
COMMENT
    : POUND .*? ('\n' | EOF)
    -> skip;
WHITESPACE
    : [ \t\r\n]+
    -> skip;

// Other tokens
LBRACE   : '{';
RBRACE   : '}';
LBRACKET : '[';
RBRACKET : ']';
OUT      : 'out';
FULL     : 'full';
AT       : '@';
EQUALS   : '=';

// Parser

level
    : NUMBER
    | OUT
    | FULL
    ;

system
    : ID                    # system_reference
    | AT AT NUMBER          # system_literal
    | LBRACE system+ RBRACE # system_compound
    ;

setting
    : BANG ID                # setting_reference
    | system AT level        # setting_literal
    | LBRACE setting+ RBRACE # setting_compound
    ;

sequence
    : DOLLARS ID                 # sequence_reference
    | LBRACKET setting+ RBRACKET # sequence_literal
    ;

declaration
    : ID EQUALS system           # system_declaration
    | BANG ID EQUALS setting     # setting_declaration
    | DOLLARS ID EQUALS sequence # sequence_declaration
    ;
