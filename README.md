# lxscript
Entertainment lighting control language

## Syntax Overview

```
show
patch
    1 @ 1
    2 @ 2
    3 @ 3
    
    4 @ 101
    5 @ 102

preset foo
    1 @ full
    2 @ out
    3 @ 50

import bar

preset blackout stage

sequence main
    0 blackout
    5 foo
    1 bar
    10 blackout
```

### Showfiles and Other Files
An lxscript showfile contains a show declaration:

```
show
```

This is followed by any number of imports, declarations, or actions.

Alternately, a file can contain a single declaration, which can then be imported into a showfile.

### Declarations

#### Patch

A patch declaration creates channels and maps them to addresses:

```
patch
    [channel] @ [address]
    ...
```

`[channel]` is the channel number, and `[address]` is the DMX address to patch the channel to.