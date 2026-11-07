#!/usr/bin/env python3
"""melonDS's GLSL 1.40 shaders as GLSL ES 3.20 for 游典's Android build (OpenGL ES 3.2), written to
melonDS/src/OpenGL_shaders/es/: compiled to SPIR-V by glslangValidator (desktop GLSL, whose implicit
int/float conversions ES doesn't have), then back to GLSL ES by SPIRV-Cross, with every conversion
spelled out. Locations are taken out again: the attributes are bound by name in C++
(glBindAttribLocation), the stages' in/out match by name, and ToGLES gives each fragment output
its location. 3DRender's W-buffer variant (#define WBuffer) is written as 3DRender?S_W.
Run after changing a shader; the result is committed."""
import glob, os, re, subprocess, sys, tempfile
root = os.path.expanduser('~/code/youdian-cores/melonDS/src/OpenGL_shaders')
out_dir = os.path.join(root, 'es')
os.makedirs(out_dir, exist_ok=True)

def convert(src, stage, name):
    src = re.sub(r'#version[^\n]*\n', '#version 450\n', src, count=1)
    with tempfile.TemporaryDirectory() as d:
        inp, spv = os.path.join(d, 'a.' + stage), os.path.join(d, 'a.spv')
        open(inp, 'w').write(src)
        r = subprocess.run(['glslangValidator', '-G', '--auto-map-locations', '--auto-map-bindings', '-o', spv, inp],
                           capture_output=True, text=True)
        if r.returncode:
            sys.exit(f'{name}: glslang\n{r.stdout}{r.stderr}')
        r = subprocess.run(['spirv-cross', spv, '--es', '--version', '320'], capture_output=True, text=True)
        if r.returncode:
            sys.exit(f'{name}: spirv-cross\n{r.stderr}')
    es = r.stdout
    # SPIRV-Cross's default float precision for fragment shaders is mediump: depth and colours want highp.
    es = es.replace('precision mediump', 'precision highp')
    # in/out: no location (by name); uniforms keep their names, their bindings set in C++.
    es = re.sub(r'(?m)^layout\(location = \d+\) ((?:flat |smooth |noperspective )?(?:in|out) )', r'\1', es)
    # Uniforms: no location or binding either (each stage numbers its own, which may not agree);
    # C++ sets the samplers' units (glUniform1i) and the blocks' bindings (glUniformBlockBinding).
    def strip(m):
        parts = [p.strip() for p in m.group(1).split(',') if not re.match(r'\s*(location|binding)\s*=', p)]
        return (f'layout({", ".join(parts)}) ' if parts else '') + 'uniform '
    es = re.sub(r'layout\(([^)]*)\) uniform ', strip, es)
    return es

n = 0
for f in sorted(glob.glob(os.path.join(root, '*.glsl'))):
    name = os.path.basename(f)[:-5]
    stage = 'frag' if name.endswith('FS') else 'vert'
    src = open(f).read()
    variants = [(name, src)]
    if name.startswith('3DRender'):
        i = src.find('\n') + 1
        variants.append((name + '_W', src[:i] + '#define WBuffer\n' + src[i:]))
    for out_name, s in variants:
        open(os.path.join(out_dir, out_name + '.glsl'), 'w').write(convert(s, stage, out_name))
        n += 1
print(f'{n} shaders written to {out_dir}')

# melonDS DS's own screen shaders, the same way, to melonds-ds/src/libretro/glsl/es/.
ds = os.path.expanduser('~/code/youdian-cores/melonds-ds/src/libretro/glsl')
os.makedirs(os.path.join(ds, 'es'), exist_ok=True)
for f, stage in (('melondsds.vert', 'vert'), ('melondsds.frag', 'frag')):
    open(os.path.join(ds, 'es', f), 'w').write(convert(open(os.path.join(ds, f)).read(), stage, f))
print('melondsds.vert/.frag written to', os.path.join(ds, 'es'))
