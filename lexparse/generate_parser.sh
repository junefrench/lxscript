#!/bin/sh
antlr4 -Dlanguage=Python3 -no-listener -visitor LXScript.g4 -o _gen
