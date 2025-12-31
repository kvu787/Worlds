shader_type spatial;
render_mode unshaded;

#include "res://Shaders/Inc/Colors.gdshaderinc"

uniform vec4 _BASE_COLOR : source_color = __BLUE;

void fragment() {
	ALBEDO = _BASE_COLOR.rgb;
}
