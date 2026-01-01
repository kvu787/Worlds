#ifndef MATH_INC
#define MATH_INC

#include "res://Shaders/Inc/Schlick.gdshaderinc"

float MapRange(float t, float aStart, float aEnd, float bStart, float bEnd) {
	return ((bEnd - bStart) / (aEnd - aStart)) * (t - aStart) + bStart;
}

float GetRadius(vec2 xy) {
	return sqrt(pow(xy.x, 2) + pow(xy.y, 2));
}

vec2 RotateXY(vec2 xy, float angle) {
    float s = sin(angle);
    float c = cos(angle);
    // Standard CCW Matrix: [ c  -s ]
    //                      [ s   c ]
    // GLSL Column-Major: vec2(c, s), vec2(-s, c)
    mat2 rotation_matrix = mat2(vec2(c, s), vec2(-s, c));
    return rotation_matrix * xy;
}

#endif
