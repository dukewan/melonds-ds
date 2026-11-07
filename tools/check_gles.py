#!/usr/bin/env python3
"""Every melonDS / melonDS DS shader, as OpenGLSupport's ToGLES hands it to OpenGL ES 3.2, through
glslangValidator: the errors an Android GPU would report, without a device."""
import glob, os, re, subprocess, sys, tempfile
HEAD = ("#version 320 es\nprecision highp float;\nprecision highp int;\nprecision highp sampler2D;\n"
        "precision highp usampler2D;\nprecision highp isampler2D;\nprecision highp sampler2DArray;\n"
        "precision highp usampler2DArray;\nprecision highp sampler3D;\n")
root = os.path.expanduser('~/code/youdian-cores')
files = sorted(glob.glob(f'{root}/melonDS/src/OpenGL_shaders/es/*.glsl')) + \
        [f'{root}/melonds-ds/src/libretro/glsl/es/melondsds.vert', f'{root}/melonds-ds/src/libretro/glsl/es/melondsds.frag']
bad = 0
for f in files:
    src = open(f).read()
    name = os.path.basename(f)
    stage = 'frag' if re.search(r'FS\.glsl$|\.frag$', name) else 'vert'
    variants = [('', src)]
    if False:
        i = src.find('\n') + 1
        variants.append(('W', src[:i] + '#define WBuffer\n' + src[i:]))
    for tag, s in variants:
        s = re.sub(r'#version[^\n]*\n', HEAD, s, count=1)
        if stage == 'frag':
            n = iter(range(8))
            s = re.sub(r'(?m)^out ', lambda m: f'layout(location = {next(n)}) out ', s)
        with tempfile.NamedTemporaryFile('w', suffix='.' + stage, delete=False) as t:
            t.write(s)
        r = subprocess.run(['glslangValidator', t.name], capture_output=True, text=True)
        os.unlink(t.name)
        errs = [l for l in r.stdout.splitlines() if 'ERROR' in l and 'compilation errors' not in l]
        if errs:
            bad += 1
            print(f'== {name}{tag}')
            for l in errs[:12]:
                print('  ', l.replace(t.name, ''))
print(f'{len(files)} files, {bad} with errors')
