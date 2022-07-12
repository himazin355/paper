# Paper
A new markup language.
## Requirements
* Basic use: Python
## PFO Format
### Standard
* One blank line represents `<br>`.
* `//` Disable one line of parging.
* `||` is a one-line comment, omitted at compile time.
### Special Variables
* `{{ss}}` for `//`
* `{{ll}}` for `||`
* {{cYear}}, {{cMonth}}, {{cDay}}, {{cHour}}, {{cMinute}} - The time when the page was compiled at.
### Custom tags
Custom tags‘re defined with regex and replacer. 
Replacer is a function that takes a converter as a positional argument and regular expression matched items as arguments and kwargs. 
It can also pass a string. 
If a string is passed, `{0}` is replaced by the first argument, and args and kwargs’re replaced thereafter. 
Only one custom tag is written per line.
## Usage
### setup.py
`setup.py` must define the function `get_compiler()`. 
It takes no arguments and must return an instance of compiler.
You may want to add a tag there.

You can use these hooks:
* `before_compile(compiler)`
* `before_folder_write(compiler, dirname, filename)`
* `before_file_write(compiler, filename)`
* `after_compile(compiler)`
## GenericData
`Compiler.misc` is GenericData. 
It can be used when you want to use values between tags and hooks.
## CLI
This is a CLI-based utility, so use it like python3 `compiler.py` `<dirname-or-filename>`. 
Dirname will compile files in that directory with a `.pfo` extension.

The compiled file will have the extension `.html`.

