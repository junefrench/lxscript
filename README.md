# lxscript
Entertainment lighting control language

## Syntax Overview

The basic primitives in lxscript are 'systems', 'settings', and 'sequences'. A system represents any collection of lighting instruments, from a single instrument to an entire rig. The concept of a 'system' includes both the 'channel' and 'group' concepts from more traditional lighting control systems. A setting represents some settings for a specific system. A setting corresponds to a 'palette' or 'preset' on a traditional lighting console. A 'sequence' is a list of settings. This is like a 'chase' or 'cue list' on a traditional console. 
### Systems

Systems are defined by giving them a name and assigning some other systems to them. The name is of the format `([\w_]+\d* | \d+)` (an ID of letters and underscores with an optional number, or just a number). A system is declared with `name = system` or `name = {system, system, ...}`. This allows new systems to be built up from existing systems. 

There is also a concept of a 'system literal'. This is how patching systems to actual lighting fixtures is accomplished. A system literal takes the form `type @ address`, where `type` is the type of fixture and `address` is the starting DMX address.

In the initial version there will be no types. Instead of `type @ address` just use `@@ address`. All literals are just dimmers.

```
1 = +dim@1 # system 1 is a dimmer at address 1
2 = +dim@2
3 = +dim@3
led1 = +rgb@101 # system led1 is an rgb fixture at address 101
led2 = +rgb@104
led3 = +rgb@107
house = {+dim@51 +dim@52 +dim@53 +dim@54} # system house includes four different dimmers

front = {1 2 3} # system front is a group including systems 1, 2, and 3
leds = {led1 led2 led3}
```

### Settings

Settings are defined much like systems (by building them up out of existing settings) except that their names always begin with a `!` character.

Also like systems, there is a setting literal. A setting literal has several forms. The most basic is `system @ level`, for example `1 @ 50` to set system 1 at 50% intensity. A slightly more advanced type of setting sets a specific parameter, which is useful for intelligent fixtures. This takes the form `system.parameter @ value`. For example `1.intensity @ 50` would be equivalent to the previous example. 

For non-intensity parameters the appropriate type of value must be used. For intensity this is the 'level' (a number from 0 to 100, or 'full', or 'out'). An example of another parameter type might be color; a color could take the form `%level.level.level` (three levels for red, green, and blue).

Initial work will not support parameters, only basic levels. Parameters will be added eventually.

```
# Looks
!blackout = {
    # setting blackout is all channels out
    front @ out
    leds @ out
    house @ out
}

# LED colors
!red = leds.color @ %full.out.out
!orange = leds.color @ %full.50.out

# Cues
!1 = {
    !blackout
    # settings appearing later in this setting will override earlier ones.
    # so, blackout will set everything out, but then we can override a few systems.
    1 @ 50
    2 @ full
    3 @ 50
}

!2 = {
    !red # all leds at red, could also say 'leds @ !red' but that's redundant in this case
    led2 @ !orange # overrides previous color from !red
}
```

### Sequences

Sequences are named with a leading `$` character, and defined thus: `name = [setting setting ...]`. 

Obviously at some point we'll need timing info. Not sure on the best way to do that.

```
$main = [!blackout !1 !2 !blackout] # a cue list
$check = [
    # This would bring on fixtures to 10% one at a time for dimmer check
    1 @ 10
    2 @ 10
    3 @ 10
    {
        # take out all conventionals and bring up the first LED
        !blackout
        led1 @ 10
    }
    led2 @ 10
    led3 @ 10
]
```
