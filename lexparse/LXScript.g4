grammar LXScript;

// Lexer

// Keywords and special characters
LBRACE   : '{';
RBRACE   : '}';
LBRACKET : '[';
RBRACKET : ']';
OUT      : 'out';
FULL     : 'full';
AT       : '@';
EQUALS   : '=';

// Sigils for different types of IDs
BANG    : '!'; // Setting
DOLLARS : '$'; // Sequence

NUMBER
    : [0-9]+
    ;

NAME
    : [A-Za-z_]+
    ;

// Comments and whitespace
COMMENT
    : '#' .*? ('\n' | EOF)
    -> skip;
WHITESPACE
    : [ \t\r\n]+
    -> skip;

// Parser

identifier
    : NAME NUMBER?
    | NUMBER
    ;

level
    : NUMBER
    | OUT
    | FULL
    ;

system
    : identifier            # system_reference
    | AT AT NUMBER          # system_literal
    | LBRACE system+ RBRACE # system_compound
    ;

setting
    : BANG identifier        # setting_reference
    | system AT level        # setting_literal
    | LBRACE setting+ RBRACE # setting_compound
    ;

sequence
    : DOLLARS identifier                 # sequence_reference
    | LBRACKET setting+ RBRACKET         # sequence_literal
    ;

declaration
    : identifier EQUALS system           # system_declaration
    | BANG identifier EQUALS setting     # setting_declaration
    | DOLLARS identifier EQUALS sequence # sequence_declaration
    ;
