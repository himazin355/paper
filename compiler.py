### PaperFormat Compiler

import re, datetime

def assign(items, fill):
    if isinstance(items, dict):
        filler = fill.copy()
        return filler.update(items or {}) or {}
    return [fill[i] if i > len(items) - 1  or items[i] is None else items[i] for i in range(max(len(fill), len(items)))]

class GenericData:
    def __init__(self, _, **data):
        self.__dict__.update(data)

    def __repr__(self):
        result = '<GenericData: '
        result += repr(self.__dict__)
        result += '>'
        return result

    __str__ = __repr__

    def __getitem__(self, key):
        return self.__dict__.__getitem__(key)

    def __setitem__(self, key, val):
        return self.__dict__.__setitem__(key, val)

    def __delitem__(self, key):
        return self.__dict__.__delitem__(key)

class Compiler:
    def __init__(self):
        self.tags = {}
        self.misc = GenericData(None, **{})

    def add_tag(self, regex, to, *, default_arg=[], default_kwarg={}):
        if isinstance(to, str):
            _to = to
            def to(_, *args, **kwargs):
                print(assign(args, default_arg))
                print(assign(kwargs, default_kwarg))
                return _to.format(*assign(args,default_arg), **assign(kwargs,default_kwarg))
        self.tags[re.compile(regex)] = to


    def default_parser(self, text):
        now = datetime.datetime.now()
        return text.replace("{{ss}}","//") \
                   .replace("{{ll}}","||") \
                   .replace("{{cMonth}}",str(now.month)) \
                   .replace("{{cDay}}",str(now.day)) \
                   .replace("{{cYear}}",str(now.year)) \
                   .replace("{{cHour}}",str(now.hour)) \
                   .replace("{{cMinute}}",str(now.minute))

    def parse(self, text):
        val = "<html>"
        for line in text.split("\n"):
            if line.startswith("//"):
                val += line.replace("//","",1)
                continue
            elif line.startswith("||"):
                continue
            elif line == "":
                val += "<br>"
            else:
                line = self.default_parser(line)
                for tag, to in self.tags.items():
                    def wrapper(match):
                        return to(self, *match.groups(), **match.groupdict())
                    line = tag.sub(wrapper, line)
                val += line
        return val + "</body></html>"

    def parse_file(self, fp):
        text = self.parse(fp.read())
        fp.seek(0)
        fp.write(text)
        fp.seek(0)

if __name__ == '__main__':
    import argparse, os
    parser = argparse.ArgumentParser(description='Compiles .pfo file.')
    parser.add_argument("file", help="compiles the given file.")
    args = parser.parse_args()

    import setup
    compiler = setup.get_compiler()

    if hasattr(setup, "before_compile"):
        setup.before_compile(compiler)

    if os.path.exists(args.file):
        if os.path.isdir(args.file):
            for file in os.listdir(args.file):
                if file.endswith(".pfo"):
                    if hasattr(setup, "before_folder_write"):
                        setup.before_folder_write(compiler, args.file, file)
                    with open(os.path.join(args.file, file), "r+", encoding="utf-8") as fp:
                        compiler.parse_file(fp)
                    os.rename(os.path.join(f"./{args.file}/", file), os.path.join(f"./{args.file}/", file.replace(".pfo",".html")))
        else:
            if hasattr(setup, "before_file_write"):
                setup.before_file_write(compiler, args.file)
            with open(args.file, "r+", encoding="utf-8") as fp:
                compiler.parse_file(fp)
            os.rename(args.file, args.file.replace(".pfo",".html"))
        if hasattr(setup, "after_compile"):
            setup.after_compile(compiler)
