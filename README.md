yamlgen
=======

#### A generator for YAML files that supports recursive inclusions and variables

### Inclusions

yamlgen generates YAML (.yml) files from YAML generator (.yg) files that support
an include directive of the following form: 

> `!include "<.yg or .yml file>"`

The path to included files can be relative to the including file or absolute.

Any inclusions in included .yg files will be recursively resolved.

The include directive can appear at any indentation level. If indented,
the included file inherits the respective indentation and the indentation
will be appended appropriately.

Generated .yml files will be placed in the same directory as the input files.

### Variables

YAML generator files may contain string variable definitions, and these variables can
be referenced later.

> `!${varname} = "value"`

To reference a variable simply use the expression !${varname} in your .yg files.

