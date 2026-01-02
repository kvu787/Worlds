shader_type spatial;
render_mode unshaded;

#include "res://Shaders/Inc/Colors.gdshaderinc"
#include "res://Shaders/Inc/Numbers.gdshaderinc"

uniform vec4 _BASE_COLOR : source_color = __BLUE;
uniform bool _LOCK_TO_WORLD_SPACE = false;
uniform float _magnitude : hint_range(0.0, 1.0) = 0.0625;

void fragment() {
	vec3 normal;
	if (_LOCK_TO_WORLD_SPACE) {
		normal = normalize((INV_VIEW_MATRIX * vec4(NORMAL, 0.0)).xyz);
	} else {
		normal = normalize(NORMAL);
	}

	// ALBEDO = _BASE_COLOR.rgb + _magnitude * (normal - vec3(__COSINE_MAGIC_ANGLE));
	//ALBEDO = _BASE_COLOR.rgb + _magnitude * (normal - vec3(1));
	ALBEDO = _BASE_COLOR.rgb + _magnitude * -normal;
}
