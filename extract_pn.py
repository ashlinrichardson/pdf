#!/usr/bin/env python
'''this script run from work_queue.txt'''
import os
import sys


def run(cmd):
    print cmd
    a = os.system(cmd)
    if a != 0:
        print "error: could not run command"
        sys.exit(1)
    return a


if len(sys.argv) < 3:
    print "extract_pn [page number, 0 indexed] [ pdf file]"
    sys.exit(1)

i, fn = None, None
try:
    i = int(sys.argv[1])
    fn = sys.argv[2]
except err:
    print "could not parse", sys.argv[1]
    sys.exit(1)


def filter_func(char):
    return char == '\n' or 48 <= ord(char) <= 57


p_n = {}
for res in range(2, 6):
    png_fn = "./.pages/p" + str(i+1)+".png"
    run("convert -density " + str(int(res) * 50) + "x" + str(int(res)*50) +
        " -units PixelsPerInch -gravity South -crop 100%x4.35% +repage " +
        fn + "[" + str(i) + "] " + png_fn)

    png_l = "./.pages/L" + str(i + 1) + ".png"
    png_r = "./.pages/R" + str(i + 1) + ".png"

    run("convert -gravity West -crop 6%x100% +repage " + png_fn + " " + png_l)

    r_str = l_str = None
    try:
        run("rm -f tl.txt")
        run("tesseract " + png_l + " --psm 6 " + "tl")
        l_str = filter(filter_func, open("tl.txt").read().strip()).lower()
    except err:
        x = os.popen("gocr " + png_l + " -C 0-9").read()
        l_str = filter(filter_func, x.strip()).lower()

    run("convert -gravity East -crop 6%x100% +repage " + png_fn + " " + png_r)

    try:
        run("rm -f tr.txt")
        run("tesseract " + png_r + " --psm 6 " + "tr")
        r_str = filter(filter_func, open("tr.txt").read().strip()).lower()

    except err:
        x = os.popen("gocr " + png_r + " -C 0-9").read()
        r_str = filter(filter_func, x.strip()).lower()

    print "[" + l_str + "," + r_str + "]"
    try:
        LL = int(l_str)
        if LL in p_n:
            p_n[LL] += 1
        else:
            p_n[LL] = 1
    except err:
        pass
    # other side
    try:
        RR = int(r_str)
        if RR in p_n:
            p_n[RR] += 1
        else:
            p_n[RR] = 1
    except err:
        pass

max_i = None
max_c = None
for k in p_n:
    if max_c is None or p_n[k] > max_c:
        max_c = p_n[k]
        max_i = k

print str(max_i) + "********** " + str(p_n)

open("./.pages/n" + str(i) + ".txt", "wb").write(str(max_i))
open("./.pages/n" + str(i) + "_dbg.txt", "wb").write(str(p_n))
