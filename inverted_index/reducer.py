#!/usr/bin/env python

from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None
dict = {}

for line in sys.stdin:
    line = line.strip()

    filename, word = line.split()
    if word not in dict:
        dict[word] = [filename]
    else:
	if dict[word].count(filename) == 0:
            dict[word].append(filename) 
    
for k in dict:
    print '%s %s' % (k, ",".join(dict[k]))
