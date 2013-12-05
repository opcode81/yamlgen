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
the an include directory of the following form: !include "<.yg or .yml file>"

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
        self.path, self.filename = os.path.split(ygFilePath.replace("/", os.path.sep))   
        if self.filename[-3:] != ".yg": raise Exception("Not a .yg file: %s" % ygFilePath)
        self.patIncludeLine = re.compile(r'''^(\s*!include\s+".*?"\s*$)''', re.MULTILINE)   

    def include(self, match, path):
        match = re.search(r'''(\s*)!include\s+"(.*?)"''', match.group(1))
        indentation = match.group(1)
        includedFile = match.group(2).replace("/", os.path.sep)
        if not os.path.exists(includedFile):
            includedFile = os.path.join(path, includedFile)
            if not os.path.exists(includedFile):
                raise Exception("Could not find inclusion '%s'" % match.group(1))
        print "  including %s" % includedFile
        text = self._gen(*os.path.split(includedFile))
        lines = text.split("\n")
        return "\n".join(map(lambda l: indentation + l, lines))                
    
    def _gen(self, path, filename):
        fullpath = os.path.join(path, filename)
        print fullpath
        text = file(fullpath, "r").read()
        return self.patIncludeLine.sub(lambda match, path=path: self.include(match, path), text)

    def gen(self):
        text = self._gen(self.path, self.filename)
        outfile = os.path.join(self.path, self.filename.replace(".yg", ".yml"))
        print "writing %s" % outfile
        with file(outfile, "w") as f:
            f.write(text)
        
if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-i", dest="file", help="the .yg input file", metavar="<file>", type="string")
    (options, args) = parser.parse_args()
    if options.file is not None:
        YamlGen(options.file).gen()
    