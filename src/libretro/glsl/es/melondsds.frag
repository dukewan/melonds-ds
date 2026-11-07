#version 320 es
precision highp float;
precision highp int;

layout(std140) uniform uConfig
{
    highp vec2 uScreenSize;
    uint u3DScale;
    uint uFilterMode;
    highp vec4 cursorPos;
    uint cursorVisible;
} _32;

uniform highp sampler2DArray ScreenTex;

in highp vec3 fTexcoord;
out highp vec4 oColor;

void main()
{
    highp vec4 pixel = texture(ScreenTex, fTexcoord);
    highp vec2 fragPos = vec2(gl_FragCoord.x, _32.uScreenSize.y - gl_FragCoord.y);
    bool _48 = _32.cursorVisible != 0u;
    bool _58;
    if (_48)
    {
        _58 = _32.cursorPos.x <= fragPos.x;
    }
    else
    {
        _58 = _48;
    }
    bool _66;
    if (_58)
    {
        _66 = _32.cursorPos.y <= fragPos.y;
    }
    else
    {
        _66 = _58;
    }
    bool _75;
    if (_66)
    {
        _75 = _32.cursorPos.z >= fragPos.x;
    }
    else
    {
        _75 = _66;
    }
    bool _84;
    if (_75)
    {
        _84 = _32.cursorPos.w >= fragPos.y;
    }
    else
    {
        _84 = _75;
    }
    if (_84)
    {
        pixel = vec4(1.0 - pixel.x, 1.0 - pixel.y, 1.0 - pixel.z, pixel.w);
    }
    oColor = vec4(pixel.xyz, 1.0);
}

