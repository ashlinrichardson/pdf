#!/usr/bin/env python
'''run this script, then run "multicore work_queue.txt".
then run collect_pn.py'''
import os
import sys

fn = "hunting-trapping-synopsis-2018-2020.pdf"

if len(os.popen("convert -version").read().split("ImageMagick")) < 2:
    print "error: could not find ImageMagick installation"
    sys.exit(1)

if os.system("pdfinfo -v") != 0:
    print "error: can't find pdfinfo"
    sys.exit(1)

n_pg = None
for line in os.popen("pdfinfo " + fn).read().split('\n'):
    if line[0:5] == "Pages":
        n_pg = int(line.strip().split()[1])

print n_pg

os.system("mkdir -p ./.pages/")

f = open("work_queue.txt", "wb")

for i in range(0, n_pg):
    # set up extract_pn.py
    cmd = "python extract_pn.py " + str(i) + " " + fn
    print cmd
    f.write(cmd + "\n")

f.close()
