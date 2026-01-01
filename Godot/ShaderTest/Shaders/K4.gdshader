shader_type spatial;
render_mode unshaded;

#include "res://Shaders/Inc/Colors.gdshaderinc"
#include "res://Shaders/Inc/Math.gdshaderinc"
#include "res://Shaders/Inc/Numbers.gdshaderinc"
#include "res://Shaders/Inc/Schlick.gdshaderinc"

const float Z_EPSILON = 0.0001;

uniform vec4 _BASE_COLOR : source_color = __BLUE;
uniform float _BASE_COLOR_POSITION : hint_range(0.0, 1.0) = __COSINE_37_DEG;
uniform float _SHIFT : hint_range(0.0, 1.0) = 0.0;
uniform float _ROTATION : hint_range(0.0, 360.0) = 0.0;
uniform float _DARKEN_RATIO : hint_range(0.0, 1.0) = 1.0;
uniform float _LIGHTEN_RATIO : hint_range(0.0, 1.0) = 1.0;

float ZComponent(float x, float y) {
	return sqrt(1.0 - x*x - y*y);
}

float XComponent(float y, float z) {
	return sqrt(1.0 - y*y - z*z);
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
	vec2 rotatedNormalXY = RotateXY(normal.xy, -1.0 * _ROTATION * PI / 180.0);
	float remappedFacingRatio = RemapFacingRatio(rotatedNormalXY.x, rotatedNormalXY.y, normal.z, _SHIFT);
	float facingRatioPositionOfBaseColor = _BASE_COLOR_POSITION;
	vec3 darkPoint = mix(_BASE_COLOR.rgb, vec3(0.0, 0.0, 0.0), _DARKEN_RATIO);
	vec3 lightPoint = mix(_BASE_COLOR.rgb, vec3(1.0, 1.0, 1.0), _LIGHTEN_RATIO);

	ALBEDO = vec3(
		SchlickABCD(remappedFacingRatio, facingRatioPositionOfBaseColor, _BASE_COLOR.r, darkPoint.r, lightPoint.r),
		SchlickABCD(remappedFacingRatio, facingRatioPositionOfBaseColor, _BASE_COLOR.g, darkPoint.g, lightPoint.g),
		SchlickABCD(remappedFacingRatio, facingRatioPositionOfBaseColor, _BASE_COLOR.b, darkPoint.b, lightPoint.b));
}
