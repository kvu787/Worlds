shader_type spatial;
render_mode unshaded;
//render_mode cull_disabled;

uniform vec3 target_direction = vec3(1.0, 1.0, 1.0);

void fragment() {
	// 1. Transform the NORMAL from View Space to World Space
	// VIEW_MATRIX is the camera's orientation.
	// We multiply the matrix by the normal to get the direction in the world.
	vec3 world_normal = normalize((INV_VIEW_MATRIX * vec4(NORMAL, 0.0)).xyz);

	// 2. Normalize our target direction
	vec3 light_dir = normalize(target_direction);

	// 3. Calculate Dot Product using the World Normal
	float dot_prod = dot(world_normal, light_dir);

	// 4. Clamp and Output
	float intensity = clamp(dot_prod, 0.0, 1.0);
	ALBEDO = intensity * vec3(1.0, 1.0, 1.0);

	//if (!FRONT_FACING) {
		//ALBEDO = vec3(0.0, 1.0, 0.0); // Green on the inside
	//}
}
