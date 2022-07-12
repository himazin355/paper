import os, subprocess, re, hashlib, scratchapi2

def get_avatar(conv, username, *args, **kwargs):
    avatar_url = scratchapi2.User(username).images["90x90"]
    return f"<img src='{avatar_url}' class='avatar' alt='Avatar of {username}'>"

def handle_image(conv, fname, *args, **kwargs):
    return f"<img src='./static/{conv.misc.changed_images[fname]}'>"

def get_compiler():
    import compiler
    cmp = compiler.Compiler()
    cmp.misc.changed_images = {}
    cmp.add_tag("{{Meta(?:|\|([^}]*))}}", "<head><meta charset='utf-8'><title>{0}</title></head><body>", default_arg=("No title","Foo","Bar"))
    cmp.add_tag("{{img\|([^}]+)}}", handle_image)
    cmp.add_tag("{{avatar\|([a-zA-Z0-9_-]+)}}", get_avatar)
    return cmp

MD5ED_REGEX = re.compile("[0-9a-f]{32}\.[pP][nN][gG]")

def check_statics(compiler):
    for file in os.listdir("./pages/static"):
        if os.path.isfile(os.path.join("./pages/static", file)) and file.lower().endswith(".png"):
            if MD5ED_REGEX.match(file):
                continue
            else:
                print(f"Compressing file {file}")
                sp = subprocess.Popen(r'pngquant --ext .png --strip --skip-if-larger --quality 50-80 --force -- ".\pages\static\{}"'.format(file), shell=True)
                sp.wait()
                with open(os.path.join("./pages/static", file), "rb") as fp:
                    md5 = hashlib.md5(fp.read()).hexdigest() + ".png"
                compiler.misc.changed_images[file] = md5
                if os.path.exists(os.path.join("./pages/static", md5)):
                    os.remove(os.path.join("./pages/static", file))
                    continue
                os.rename(os.path.join("./pages/static", file), os.path.join("./pages/static", md5))

def before_compile(compiler):
    check_statics(compiler)
