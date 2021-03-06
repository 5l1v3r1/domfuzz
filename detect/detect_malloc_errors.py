#!/usr/bin/env python

from __future__ import absolute_import

# Look for "szone_error" (Tiger), "malloc_error_break" (Leopard), "MallocHelp" (?)
# which are signs of malloc being unhappy (double free, out-of-memory, etc).

pline = ""
ppline = ""

def amiss(logPrefix):
    foundSomething = False
    global pline, ppline

    pline = ""
    ppline = ""

    with open(logPrefix + "-err.txt") as f:
        for line in f:
            if scanLine(line):
                foundSomething = True
                break # Don't flood the log with repeated malloc failures

    return foundSomething


def scanLine(line):
    global ppline, pline

    line = line.strip("\x07").rstrip("\n")

    if (-1 != line.find("szone_error")
     or -1 != line.find("malloc_error_break")
     or -1 != line.find("MallocHelp")):
        if (-1 == pline.find("can't allocate region")):
            print ""
            print ppline
            print pline
            print line
            return True

    ppline = pline
    pline = line
