#! /usr/bin/env python3
"""
Created on Thu Sep 29 18:07:04 2022

@author: Hatim.Thayyil
@licence: MIT
"""

# ---------------------------------------------------------------
# Tanzil XML to FoLiA converter
#   by Hatim Thayyil
#
#   Licensed under MIT
# ----------------------------------------------------------------

import sys
import os
import getopt
import folia.main as folia
from lxml import etree

VERSION = "0.1.0"


def usage():
    print("tanzil2folia", file=sys.stderr)
    print("  by Hatim Thayyil (hatimbt)", file=sys.stderr)
    print("  2022 - Licensed under MIT", file=sys.stderr)
    print("", file=sys.stderr)
    print(__doc__, file=sys.stderr)
    print("", file=sys.stderr)
    print("Usage: tanzil2folia [options] tanzil-input folia-output",
          file=sys.stderr)


def makefoliadoc(outputfile):
    baseid = os.path.basename(outputfile).replace(
        '.folia.xml', '').replace('.xml', '')
    processor = folia.Processor.create("tanzil2folia", version=VERSION)
    foliadoc = folia.Document(id=baseid, processor=processor)

    return foliadoc


def tanzil2folia(tanzilfile, foliadoc):
    try:
        tree = etree.parse(tanzilfile, etree.XMLParser(
            collect_ids=False, huge_tree=True))
    except TypeError:
        tree = etree.parse(tanzilfile, etree.XMLParser())

    tanzilroot = tree.getroot()

    if tanzilroot.tag != 'quran':
        raise Exception("source file is not a tanzil.net quran file")

    foliatextbody = foliadoc.add(folia.Text(foliadoc, id=foliadoc.id+'.text'))
    for sura in tanzilroot:
        if sura.tag != 'sura':
            continue
        sura_division = foliatextbody.add(
            folia.Division(foliadoc, id=foliatextbody.id + ".ch." + sura.get("index")))
        sura_division.add(folia.Head(foliadoc, sura.get("name")))
        for aya in sura:
            aya_text = aya.get("text")
            aya_folia = sura_division.add(folia.Sentence, aya_text)

            aya_words = aya_text.split(' ')
            for aya_word in aya_words:
                aya_folia.add(folia.Word, aya_word)

    return foliadoc


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "-h", ["help"])
    except getopt.GetoptError as err:
        print(str(err), file=sys.stderr)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == '-h' or o == '--help':
            usage()
            sys.exit(0)
        else:
            raise Exception("No such option: " + o)

    if len(args) < 2:
        usage()
        sys.exit(2)
    else:
        tanzilfile = args[-2]
        foliafile = args[-1]

    doc = makefoliadoc(foliafile)
    doc = tanzil2folia(tanzilfile, doc)

    doc.save(foliafile)


if __name__ == "__main__":
    main()
