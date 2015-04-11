grammar LXScript;

// Parser Rules

text
    : show EOF
    | declaration EOF
    ;

show
    : SHOW ID show_element+
    ;

show_element
    : lx_import
    | declaration
    ;

lx_import
    : IMPORT ID
    ;

declaration
    : patch_declaration
    | preset_declaration
    | sequence_declaration
    ;

patch_declaration
    : PATCH patch_spec+
    ;

patch_spec
    : channel AT address
    ;

preset_declaration
    : PRESET ID setting*
    | PRESET ID capture_spec setting*
    ;

capture_spec
    : STAGE
    | CHANNEL
    ;

setting
    : channel AT level
    ;

channel
    : NUMBER
    ;

address
    : NUMBER
    ;

level
    : NUMBER
    | FULL
    | OUT
    ;

preset
    : ID
    ;

sequence_declaration
    : SEQUENCE ID step+
    ;

step
    : TIME preset
    ;

// Lexer Rules

SHOW:      'show';
PATCH:     'patch';
PRESET:    'preset';
SEQUENCE:  'sequence';
STAGE:     'stage';
CHANNEL:   'channel';
AT:        '@';
IMPORT:    'import';
FULL:      'full';
OUT:       'out';

ID
    : LETTER (LETTER | DIGIT | '_')+
    ;

NUMBER
    : DIGIT+
    ;

TIME
    : NUMBER
    | NUMBER ':' DIGIT DIGIT
    ;

LETTER
    : [A-Za-z]
    ;

DIGIT
    : [0-9]
    ;

WS
    : [ \n\t\r]+
    -> skip;