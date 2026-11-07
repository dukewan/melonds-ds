#version 320 es

layout(std140) uniform uConfig
{
    vec2 uScreenSize;
    uint u3DScale;
    uint uFilterMode;
    vec4 cursorPos;
    uint cursorVisible;
} _19;

in vec2 vPosition;
out vec3 fTexcoord;
in vec3 vTexcoord;

void main()
{
    vec2 _28 = ((vPosition * 2.0) / _19.uScreenSize) - vec2(1.0);
    vec4 fpos;
    fpos.x = _28.x;
    fpos.y = _28.y;
    fpos.y *= (-1.0);
    fpos.z = 0.0;
    fpos.w = 1.0;
    gl_Position = fpos;
    fTexcoord = vTexcoord;
}

