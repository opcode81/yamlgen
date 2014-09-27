#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# YAML Generator
#
# (C) 2013 by Dominik Jain
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

YAML Generator (C) 2013 Dominik Jain 

generates YAML (.yml) files from YAML Generator (.yg) files that support
an include directive of the following form: !include "<.yg or .yml file>"

The path to included files can be relative to the inclusing file.

Any inclusions in included .yg files will be recursively resolved.

The include directive can appear at any indentation level. If indented,
the included file inherits the respective indentation and the indentation
will be appended appropriately.

The generated .yml file will be placed in the same directory as the input file.

'''

import re
import os

class YamlGen(object):
    def __init__(self, ygFilePath):
        self.vars = {}
        self.path, self.filename = os.path.split(ygFilePath.replace("/", os.path.sep))   
        if self.filename[-3:] != ".yg": raise Exception("Not a .yg file: %s" % ygFilePath)
        self.patIncludeLine = re.compile(r'''^(\s*!include\s+".*?"\s*$)''', re.MULTILINE)
        self.patDefineVar = re.compile(r'''^(\s*!\$\{[^\}]+\}=".*?"\s*$)''', re.MULTILINE)
        self.patSubstVar = re.compile(r'''(!\$\{[^\}]+\})''', re.MULTILINE)

    def include(self, match, path):
        line = match.group(1)
        match = re.search(r'''(\s*)!include\s+"(.*?)"''', line)
        indentation = match.group(1).strip("\r\n")
        includedFile = match.group(2).replace("/", os.path.sep)
        includedFile = os.path.abspath(os.path.join(path, includedFile))
        if not os.path.exists(includedFile):
            raise Exception("Could not find inclusion '%s' referenced in include statement: %s" % (includedFile, line.strip()))
        print "  including %s" % includedFile
        text = self._gen(*os.path.split(includedFile))
        lines = text.split("\n")
        return "\n".join(map(lambda l: indentation + l, lines))                

    def defVar(self, match):
        text = match.group(1)
        m = re.search(r'''\$\{(.*?)\}="(.*?)"''', text)
        varname, value = m.groups()
        self.vars[varname] = value
        return ""

    def substVar(self, match):
        varname = re.search(r'''{(.*?)\}''', match.group(1)).group(1)
        if not varname in self.vars:
            raise Exception("undefined variable '%s'" % varname)
        return self.vars[varname]
    
    def _gen(self, path, filename):
        fullpath = os.path.abspath(os.path.join(path, filename))
        print fullpath
        text = file(fullpath, "r").read()
        text = self.patDefineVar.sub(lambda match: self.defVar(match), text)
        try:
            text = self.patSubstVar.sub(lambda match: self.substVar(match), text)
        except Exception as e:
            raise Exception("error while substituting variables in %s: %s" % (fullpath, str(e)))
        try: 
            ret = self.patIncludeLine.sub(lambda match, path=path: self.include(match, path), text)
        except Exception as e:
            raise Exception("error while including file in %s: %s" % (fullpath, str(e)))
        return ret

    def gen(self):
        text = self._gen(self.path, self.filename)
        outfile = os.path.join(self.path, self.filename.replace(".yg", ".yml"))
        print "writing %s" % outfile
        with file(outfile, "w") as f:
            f.write(text)
        if "\t" in text:
            pos = text.find("\t")
            raise Exception("Generated file %s contains tabs at position %d: %s" % (outfile, pos, text[pos:][:100] + "..."))
        
if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-i", dest="file", help="the .yg input file or comma-separated list of files", metavar="<file>", type="string")
    (options, args) = parser.parse_args()
    if options.file is not None:
        for filename in options.file.split(","):
            YamlGen(filename).gen()
