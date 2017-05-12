#!/usr/bin/env python3

t = int(input())

for caso in range(t):
    (a, b) = [int(x) for x in input().split(" ")]
    print("Case #", caso, ": ", a + b, sep='')
