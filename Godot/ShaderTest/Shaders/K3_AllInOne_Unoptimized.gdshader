/*
	MIT License

	Copyright (c) 2026 K

	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in all
	copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	SOFTWARE.
*/

shader_type spatial;
render_mode unshaded;

#define __BLUE vec4(0.039215688, 0.24705882, 0.78431374, 1)
#define __COSINE_37_DEG 0.79863551

const float Z_EPSILON = 0.0001;

uniform vec4 _BASE_COLOR : source_color = __BLUE;
uniform float _BASE_COLOR_POSITION : hint_range(0.0, 1.0) = __COSINE_37_DEG;
uniform float _SHIFT : hint_range(0.0, 1.0) = 0.0;
uniform float _ROTATION : hint_range(0.0, 360.0) = 0.0;
uniform float _DARKEN_RATIO : hint_range(0.0, 1.0) = 1.0;
uniform float _LIGHTEN_RATIO : hint_range(0.0, 1.0) = 1.0;

/*
	This is a modified form of Christophe Schlick's bias function.

	References:
	1. Graphics Gems IV, 1994, Christophe Schlick
	2. A Convenient Generalization of Schlick's Bias and Gain Function, 2020, Jonathan T. Barron
*/
float SchlickAB_Raw(float t, float a, float b) {
	float k1 = b * (1.0 - a);
	float k2 = b - a;
	float k3 = a * (1.0 - b);
	return (k1 * t) / (k2 * t + k3);
}

float SchlickAB(float t, float a, float b) {
	if (isnan(t)) { return t; }
	if (isnan(a)) { return a; }
	if (isnan(b)) { return b; }

	t = clamp(t, 0.0, 1.0);
	a = clamp(a, 0.0, 1.0);
	b = clamp(b, 0.0, 1.0);

	if ((a == 0.0) && (b == 0.0)) {
		return t;
	} else if ((a == 0.0) && (0.0 < b && b < 1.0)) {
		return 1.0;
	} else if ((a == 0.0) && (b == 1.0)) {
		return 1.0;
	} else if ((0.0 < a && a < 1.0) && (b == 0.0)) {
		return 0.0;
	} else if ((0.0 < a && a < 1.0) && (0.0 < b && b < 1.0)) {
		return SchlickAB_Raw(t, a, b);
	} else if ((0.0 < a && a < 1.0) && (b == 1.0)) {
		return 1.0;
	} else if ((a == 1.0) && (b == 0.0)) {
		return 0.0;
	} else if ((a == 1.0) && (0.0 < b && b < 1.0)) {
		return 0.0;
	} else if ((a == 1.0) && (b == 1.0)) {
		return t;
	}

	// This doesn't handle a defined case.
	return 0.0;
}

float SchlickA(float t, float a) {
	return SchlickAB(t, a, 0.5);
}

/*
	This modifies SchlickAB_Raw to be able to "squish" the output into the [c, d] range.
	Even though the output is bounded in [c, d] the curve still intersects point (a, b).
*/
float SchlickABCD_Raw(float t, float a, float b, float c, float d) {
	float k1 = d * (b - c) - a * b * (d - c);
	float k2 = a * c * (d - b);
	float k3 = (b - c) - a * (d - c);
	float k4 = a * (d - b);
	return (k1 * t + k2) / (k3 * t + k4);
}

float SchlickABCD(float t, float a, float b, float c, float d) {
	if (isnan(t)) { return t; }
	if (isnan(a)) { return a; }
	if (isnan(b)) { return b; }
	if (isnan(c)) { return c; }
	if (isnan(d)) { return d; }

	t = clamp(t, 0.0, 1.0);
	a = clamp(a, 0.0, 1.0);

	c = clamp(c, 0.0, 1.0);
	d = clamp(d, 0.0, 1.0);
	if (c > d) {
		return 0.0;
	}

	b = clamp(b, c, d);

	if ((a == 0.0) && (b == c)) {
		return (d - c) * t + c;
	} else if ((a == 0.0) && (c < b && b < d)) {
		return d;
	} else if ((a == 0.0) && (b == d)) {
		return d;
	} else if ((0.0 < a && a < 1.0) && (b == c)) {
		return c;
	} else if ((0.0 < a && a < 1.0) && (c < b && b < d)) {
		return SchlickABCD_Raw(t, a, b, c, d);
	} else if ((0.0 < a && a < 1.0) && (b == d)) {
		return d;
	} else if ((a == 1.0) && (b == c)) {
		return c;
	} else if ((a == 1.0) && (c < b && b < d)) {
		return c;
	} else if ((a == 1.0) && (b == d)) {
		return (d - c) * t + c;
	}

	// This doesn't handle a defined case.
	return 0.0;
}

float MapRange(float t, float aStart, float aEnd, float bStart, float bEnd) {
	return ((bEnd - bStart) / (aEnd - aStart)) * (t - aStart) + bStart;
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

float ZComponent(float x, float y) {
	return sqrt(max(0.0, 1.0 - x*x - y*y));
}

float XComponent(float y, float z) {
	return sqrt(max(0.0, 1.0 - y*y - z*z));
}

/*
	Typically, the FacingRatio is simply the z component of the surface normal.
	This forms a hemisphere surface with respect to x and y.

	RemapFacingRatio remaps the facing ratio such that "peak" is shifted by xShift along the positive x-axis.
	The output of RemapFacingRatio forms a surface that is smooth (infinitely differentiable) with respect to x and y.
	The remapped surface resembles a warped hemisphere.
*/
float RemapFacingRatio(float x, float y, float z, float xShift) {
	if (abs(z) < Z_EPSILON) {
		return 0.0;
	}

	float xStart = -XComponent(y, 0.0);
	float xEnd = XComponent(y, 0.0);
	float schlickT = MapRange(x, xStart, xEnd, 0.0, 1.0);
	float schlickA = MapRange(xShift, -1.0, 1.0, 0.0, 1.0);
	float schlickOut = SchlickA(schlickT, schlickA);
	float remappedX = MapRange(schlickOut, 0.0, 1.0, xStart, xEnd);
	float remappedFacingRatio = ZComponent(remappedX, y);

	return remappedFacingRatio;
}

void fragment() {
	vec3 normal = normalize(NORMAL);
	vec2 rotatedNormalXY = RotateXY(normal.xy, -1.0 * radians(_ROTATION));
	float remappedFacingRatio = RemapFacingRatio(rotatedNormalXY.x, rotatedNormalXY.y, normal.z, _SHIFT);
	float facingRatioPositionOfBaseColor = _BASE_COLOR_POSITION;
	vec3 darkPoint = mix(_BASE_COLOR.rgb, vec3(0.0, 0.0, 0.0), _DARKEN_RATIO);
	vec3 lightPoint = mix(_BASE_COLOR.rgb, vec3(1.0, 1.0, 1.0), _LIGHTEN_RATIO);

	ALBEDO = vec3(
		SchlickABCD(remappedFacingRatio, facingRatioPositionOfBaseColor, _BASE_COLOR.r, darkPoint.r, lightPoint.r),
		SchlickABCD(remappedFacingRatio, facingRatioPositionOfBaseColor, _BASE_COLOR.g, darkPoint.g, lightPoint.g),
		SchlickABCD(remappedFacingRatio, facingRatioPositionOfBaseColor, _BASE_COLOR.b, darkPoint.b, lightPoint.b));
}
