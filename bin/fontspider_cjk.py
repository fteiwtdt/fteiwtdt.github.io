#!/usr/bin/env python

import os
import sys
import argparse
import re

# Referred to `fontTools.subset'
from fontTools import subset

# Referred to https://github.com/fonttools/fonttools/blob/master/Snippets/woff2_compress.py
from fontTools.ttLib import TTFont
from fontTools.ttx import makeOutputFileName

# CJK Symbols And Punctuation : \u3000-\u303F
zh_CN_UTF8 = u"[\u3000-\u303F\u4E00-\u9FCC]"
p = re.compile(zh_CN_UTF8)


def readfile(filename):
    with open(filename, 'rb') as f:
        l = f.readline()
        while l:
            yield l
            l = f.readline()


def get_unicodes(filename):
    if not os.path.exists(filename):
        raise AttributeError('File: %s invalid' % filename)
    chars = set()
    for line in readfile(filename):
        chars.update(p.findall(line.decode('utf-8')))
    return chars


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath',
                        type=str,
                        dest='filepath',
                        default='',
                        help='CJK font filepath')
    return parser


def main(args):
    if not args.filepath:
        raise AttributeError('Please specify font filepath')
    if not os.path.exists(args.filepath):
        raise AttributeError('File: %s not found' % args.filepath)

    textfile_dir = '_posts'
    unichars = set()
    
    def walk_callback(args, dirname, fnames):
        for fname in fnames:
            unichars.update(get_unicodes(os.path.join(dirname, fname)))
    os.path.walk(textfile_dir, walk_callback, None)
    unicodes = [ord(c) for c in unichars]

    cjk_fontfile = args.filepath
    out_fontdir = 'assets/fonts'
    out_fontfile = makeOutputFileName(os.path.basename(args.filepath),
                                      outputDir=out_fontdir,
                                      extension='.woff',
                                      overWrite=True)

    options = subset.Options()
    dontLoadGlyphNames = not options.glyph_names
    font = subset.load_font(cjk_fontfile, options, dontLoadGlyphNames=dontLoadGlyphNames)
    subsetter = subset.Subsetter()
    subsetter.populate(glyphs=[], gids=[], unicodes=unicodes, text='')
    subsetter.subset(font)
    font.flavor = 'woff'
    font.save(out_fontfile, reorderTables=False)

    print('Input font: % 7d bytes: %s' % (os.path.getsize(cjk_fontfile), cjk_fontfile))
    print('Subset font: % 7d bytes: %s' % (os.path.getsize(out_fontfile), out_fontfile))


if __name__ == '__main__':
    sys.exit(main(get_parser().parse_args()))
