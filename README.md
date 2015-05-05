# lxscript
Entertainment lighting control language

## Usage

To run lxscript, you first need to generate the lexer and parser with ANTLR. You must have the ANTLR 4.5 tool installed, and then run `lexparse/generate_parser.sh`.

Once this is done, install dependancies with `pip install -r requirements.txt` and run with `./lxscript.py` (`-h` will print usage info).

By default, lxscript will use broadcast ArtNet, which might annoy your friendly local network administrators. To specify an address to send ArtNet to, use the `--address` argument.

You can also give a filename as an argument, and the contents of the file will be executed as lxscript code before enterning the interactive environment. Some example files are in the `examples` directory. The file `stage.c2s` is a [Capture](http://www.capturesweden.com) file which contains the lighting rig used for the examples and is configured to receive ArtNet.

## Syntax Overview

The basic primitives in lxscript are 'systems', 'settings', and 'sequences'. A system represents any collection of lighting instruments, from a single instrument to an entire rig. The concept of a 'system' includes both the 'channel' and 'group' concepts from more traditional lighting control systems. A setting represents some settings for a specific system. A setting corresponds to a 'palette' or 'preset' on a traditional lighting console. A 'sequence' is a list of settings. This is like a 'chase' or 'cue list' on a traditional console. 
### Systems

Systems are defined by giving them a name and assigning some other systems to them. The name is of the format `([\w_]+\d* | \d+)` (an ID of letters and underscores with an optional number, or just a number). A system is declared with `name = system` or `name = {system, system, ...}`. This allows new systems to be built up from existing systems. 

There is also a concept of a 'system literal'. This is how patching systems to actual lighting fixtures is accomplished. A system literal takes the form `@@ address`, where `address` is the starting DMX address.

```
1 = @@1 # system 1 is a dimmer at address 1
2 = @@2
3 = @@3
top1 = @@51
top2 = @@52
top3 = @@53
house = {@@51 @@52 @@53 @@54} # system house includes four different dimmers

front = {1 2 3} # system front is a group including systems 1, 2, and 3
top = {top1 top2 top3}
```

### Settings

Settings are defined much like systems (by building them up out of existing settings) except that their names always begin with a `!` character.

Also like systems, there is a setting literal. The form of a setting literal is `system @ level`, for example `1 @ 50` to set system 1 at 50% intensity.

```
!blackout = {
    # setting blackout is all channels out
    front @ out
    top @ out
    house @ out
}

!spot_sl = {
    # a setting for a certain look (a spotlight stage left)
    front @ out
    top @ out
    # later settings override earlier ones, so this overrides the setting of 1 to out in 'front @ out'
    1 @ full
}
```

### Sequences

Sequences are named with a leading `$` character, and defined thus: `name = [setting setting ...]`. 

```
$main = [
    # A simple cue list
    !blackout
    !spot_sl
    {
        front @ full
        top @ 50
    }
    front @ !blackout # recall just system front from setting blackout
    !blackout
]

$check = [
    # This would bring on fixtures to 10% one at a time for dimmer check
    {!blackout 1 @ 10}
    {!blackout 2 @ 10}
    {!blackout 3 @ 10}
    {!blackout top1 @ 10}
    {!blackout top2 @ 10}
    {!blackout top3 @ 10}
]
```
