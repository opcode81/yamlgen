yamlgen
=======

#### A generator for YAML files that supports recursive inclusions


yamlgen generates YAML (.yml) files from YAML generator (.yg) files that support
an include directive of the following form: 

> `!include "<.yg or .yml file>"`

The path to included files can be relative to the inclusing file.

Any inclusions in included .yg files will be recursively resolved.

The include directive can appear at any indentation level. If indented,
the included file inherits the respective indentation and the indentation
will be appended appropriately.

Generated .yml files will be placed in the same directory as the input files.
