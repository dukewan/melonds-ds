# melonDS DS for Android with OpenGL ES (游典)

This branch (`youdian-gles`) builds melonDS DS as an Android libretro core whose OpenGL renderer runs on
OpenGL ES 3.2, so 3D can be drawn by the phone's or handheld's GPU at a higher internal resolution.
It is the NDS core 游典 (youdian.games) downloads as `melondsgl_libretro_android.so`.

Changes, here and in [dukewan/melonDS `youdian-gles`](https://github.com/dukewan/melonDS/tree/youdian-gles):

- melonDS DS asks the frontend for an OpenGL ES 3.2 context; its screen shaders are GLSL ES (`src/libretro/glsl/es`).
- melonDS's shaders as GLSL ES 3.20 (`src/OpenGL_shaders/es`), converted by `tools/convert_gles.py`
  (glslang to SPIR-V, SPIRV-Cross back to GLSL ES); `tools/check_gles.py` validates them.
- 15-bit colours uploaded as `GL_UNSIGNED_SHORT_5_5_5_1` (ES has no `1_5_5_5_REV`), the 3D config
  written with `glBufferSubData`, the 3D polygon attributes as `GL_INT`.

Tested on an AYN Thor (Adreno 740), a Galaxy S21 (Adreno 660) and a GT78 (Mali-G76): 60 fps at 4x.

## Build

Android NDK r27, CMake, Ninja:

```sh
cmake -S . -B build-gles -G Ninja \
  -DCMAKE_TOOLCHAIN_FILE=$NDK/build/cmake/android.toolchain.cmake \
  -DANDROID_ABI=arm64-v8a -DANDROID_PLATFORM=android-24 -DCMAKE_BUILD_TYPE=Release \
  -DENABLE_OPENGL=ON -DOPENGL_PROFILE=OpenGLES3 -DMELONDS_GLES=ON
cmake --build build-gles
```

Licensed GPL-3.0, as melonDS and melonDS DS are.
