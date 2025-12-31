shader_type spatial;
render_mode unshaded;

#include "res://Shaders/Inc/Colors.gdshaderinc"
#include "res://Shaders/Inc/Math.gdshaderinc"
#include "res://Shaders/Inc/Numbers.gdshaderinc"
#include "res://Shaders/Inc/Schlick.gdshaderinc"

uniform vec4 _BASE_COLOR : source_color = __BLUE;
uniform float _FACING_RATIO_POSITION_OF_BASE_COLOR : hint_range(0.0, 1.0) = __COSINE_30_DEG;
uniform bool _ENABLE_SHADING_SHIFT = false;
uniform float _SHADING_SHIFT_RATIO : hint_range(0, 1.0) = 0.5;
uniform float _SHADING_SHIFT_ROTATION_DEGREES : hint_range(0, 360.0) = 0.0;

void fragment() {
	vec3 normal = normalize(NORMAL);

	vec2 rotatedNormalXY = RotateXY(normal.xy, -1.0 * _SHADING_SHIFT_ROTATION_DEGREES * PI / 180.0);
	float maxShadingShift = min(_FACING_RATIO_POSITION_OF_BASE_COLOR, 1.0 - _FACING_RATIO_POSITION_OF_BASE_COLOR);
	float shadingShift = float(_ENABLE_SHADING_SHIFT) * (rotatedNormalXY.x * _SHADING_SHIFT_RATIO * maxShadingShift);
	float facingRatioPositionOfBaseColorShifted = clamp(_FACING_RATIO_POSITION_OF_BASE_COLOR - shadingShift, 0.0, 1.0);

	float facingRatio = clamp(normal.z, 0.0, 1.0);

	ALBEDO = vec3(
		SchlickAB(facingRatio, facingRatioPositionOfBaseColorShifted, _BASE_COLOR.r),
		SchlickAB(facingRatio, facingRatioPositionOfBaseColorShifted, _BASE_COLOR.g),
		SchlickAB(facingRatio, facingRatioPositionOfBaseColorShifted, _BASE_COLOR.b));
}
