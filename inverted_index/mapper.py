#!/usr/bin/env python

import sys

filename = False

for line in sys.stdin:
    words = line.split()
    for word in words:
        if word.find(".") >= 0:
	    filename = word
        else:
	    print '%s %s' % (filename, word)
