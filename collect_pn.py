#!/usr/bin/env python
'''find page numbering consistent with ocr results'''
import os
import sys

fn = sys.argv[1]
n_pg = None

for line in os.popen("pdfinfo " + fn).read().split('\n'):
    if line[0:5] == "Pages":
        n_pg = int(line.strip().split()[1])

print n_pg
of = open("result.txt", "wb")
ci = last = beforelast = -1

rev = {}
for i in range(0, n_pg):
    f = "./.pages/n" + str(i) + "_dbg.txt"

    if not os.path.exists(f):
        print "error: can't find " + f

    d = open(f).read().strip() + "\n"
    d = d.strip()
    dic = {}

    # print d
    d = d.strip("{")
    d = d.strip("}")

    if d != "":
        for frag in d.split(","):
            fs = frag.split(":")
            count = fs[1].strip()
            pn = fs[0].strip()
            dic[int(pn)] = int(count)

    if (ci == -1):
        if 2 in dic:
            ci = 2
    else:
        if (last + 1) in dic:
            ci = last + 1
        else:
            if (beforelast + 2) in dic:
                ci = beforelast + 2

    pn = ci
    if ci == last:
        pn = -1

    print i, "pn=", pn, str(dic)
    of.write(str(i + 1) + "," + str(pn) + "," + str(dic) + "\n")

    if pn != -1:
        rev[pn] = i + 1

    beforelast = last
    last = ci

of.close()

print rev
