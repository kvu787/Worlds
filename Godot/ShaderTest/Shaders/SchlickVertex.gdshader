shader_type spatial;
render_mode unshaded;

uniform vec4 color : source_color = vec4(0.5, 0.5, 0.5, 1.0);
uniform float cosTheta : hint_range(0.0, 1.0) = 0.866025403784;

// Pre-calculate normalized world direction (1,1,1) constant
const vec3 WORLD_LIGHT_DIR = vec3(0.57735, 0.57735, 0.57735);

// Pass the view-space light direction from Vertex to Fragment
varying vec3 view_light_dir;

float ModifiedSchlicksBias(float a, float b, float x) {
	float c1 = b * (1.0 - a);
	float c2 = b - a;
	float c3 = a * (1.0 - b);
	return (c1 * x) / (c2 * x + c3);
}

// Logic preserved exactly as requested
float ModifiedSchlicksBias_Safe(float a, float b, float x) {
	if ((a == 0.0) && (b == 0.0)) {
		return x;
	} else if ((a == 0.0) && (0.0 < b && b < 1.0)) {
		return 1.0;
	} else if ((a == 0.0) && (b == 1.0)) {
		return 1.0;
	} else if ((0.0 < a && a < 1.0) && (b == 0.0)) {
		return 0.0;
	} else if ((0.0 < a && a < 1.0) && (0.0 < b && b < 1.0)) {
		return ModifiedSchlicksBias(a, b, x);
	} else if ((0.0 < a && a < 1.0) && (b == 1.0)) {
		return 1.0;
	} else if ((a == 1.0) && (b == 0.0)) {
		return 0.0;
	} else if ((a == 1.0) && (0.0 < b && b < 1.0)) {
		return 0.0;
	} else if ((a == 1.0) && (b == 1.0)) {
		return x;
	}
	// Fallback return to satisfy GLSL compiler strictness
	// (in case inputs float outside the explicit checks above)
	return x;
}

void vertex() {
	// OPTIMIZATION: Transform Light Direction to View Space here (Per-Vertex).
	// This replaces the expensive Per-Pixel Normal transformation.
	view_light_dir = (VIEW_MATRIX * vec4(WORLD_LIGHT_DIR, 0.0)).xyz;
}

void fragment() {
	// 1. Setup Vectors (Both are now in View Space)
	// Godot provides NORMAL in View Space by default.
	vec3 normal = normalize(NORMAL);
	vec3 light = normalize(view_light_dir);

	// 2. Calculate Dot Product
	float dot_prod = dot(normal, light);
	float facingRatio = clamp(dot_prod, 0.0, 1.0);

	// 3. Apply Bias
	// Because the logic relies on scalar if/else checks, we cannot vectorize this
	// efficiently. We must run it 3 times (R, G, B).
	ALBEDO = vec3(
		ModifiedSchlicksBias_Safe(cosTheta, color.r, facingRatio),
		ModifiedSchlicksBias_Safe(cosTheta, color.g, facingRatio),
		ModifiedSchlicksBias_Safe(cosTheta, color.b, facingRatio)
	);
}
