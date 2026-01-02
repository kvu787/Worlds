provide python code to do the following

0 <= float Hue < 360
0 <= float Saturation <= 1
0 <= float GrayScale <= 1

1. Compute "GrayscaleLength" = Grayscale * sqrt(3)
1. Compute "GrayscalePoint" = grayscale * \left(\sqrt{3},\ \sqrt{3},\ \sqrt{3}\right)
2. Compute "RadiusLimit" =

------

\left(0.18093038,0.18093038,0.63813923\right)
\left(0.3125,0.3125,0.875\right)
\left(0.51426372,0.51426372,0.97147257\right)

teal
football = \left(0.36186077,0.81906962,0.81906962\right)
colorizer = 5dd2d2
blender = A2EAEA

------

c_{1}=b\left(1-a\right)
c_{2}=b-a
c_{3}=a\left(1-b\right)
f\left(x\right)=\frac{c_{1}\cdot x}{c_{2}\cdot x+c_{3}}\ \ \ \ \ \ \ \ \ \left\{0\le x\le1\right\}

if (a == 1 && b == 1) {
  linear
} else if (a == 0 && b == 0) {
  linear
} else if (a == 0) {
  1
} else if (a == 1) {
  0
} else if (b == 0) {
  0
} else if (b == 1) {
  1
}

a = 0, 0 < a < 1, a = 1
b = 0, 0 < b < 1, b = 1

-------

i would like a custom shader that achieves the following:

(use degrees not radians)

the shader is an emission shader so basically it decides what color the pixel is that its rendering

let A be the normalized surface normal vector. let B be the direction vector representing what the camera is looking at. let T be the angle between A and B. let C be an input rgb color representing the base color.

for 90<=T<=180, don't render anything since its not visible by the camera
for 0<=T<90, we do render something

let T2 be the angle that A is rotated about B. T2 goes from 0 to 360. we define 3 "poles" in the domain of T2: P1=0 deg, P2=120 deg, P1=240 deg. P1=neutral, P2=lighten, P1=darken. The closer T2 is to a pole, the more it is affected by it. So if the pixel's T2 is between P2 and P0, then it should be darkened but not as darkened as if it were at P1.

describe the math i can use to accomplish this

$$t_{smooth} = t^2 \times (3 - 2t)$$
$$t_{smooth} = \frac{1 - \cos(t \times \pi)}{2}$$
$$t_{smooth} = \frac{1 - \cos(t \times 180)}{2}$$
$$t_{smooth}(\theta) = \frac{1 - \cos(1.5 \times \theta)}{2}$$


----
#ifndef COLOR_INC
#define COLOR_INC
#define __GRAY vec4(0.5, 0.5, 0.5, 1.0)
#define __BLUE vec4(0.039215688, 0.24705882, 0.78431374, 1)
#define __PURPLE vec4(0.4941, 0.17820002, 0.81, 1)
#define __PINK_PALE vec4(0.735357, 0.368734, 0.70975083, 1)
#define __PINK_BRIGHT vec4(0.9411765, 0.47058824, 0.9098039, 1)
#endif

#ifndef NUMBERS_INC
#define NUMBERS_INC
// cosine(30 deg) = √(3)/2 = 0.866025403784
#define __COSINE_30_DEG 0.866025403784
// cosine(MagicAngle) = cosine(arccos(1/√(3))) = 1/√(3) = 0.5773502692
#define __COSINE_MAGIC_ANGLE 0.5773502692
#endif

#ifndef SCHLICK_INC
#define SCHLICK_INC
float ModifiedSchlicksBias(float a, float b, float x) {
	float c1 = b * (1.0 - a);
	float c2 = b - a;
	float c3 = a * (1.0 - b);
	return (c1 * x) / (c2 * x + c3);
}
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
}
#endif

shader_type spatial;
render_mode unshaded;
#include "res://Shaders/Inc/Colors.gdshaderinc"
#include "res://Shaders/Inc/Numbers.gdshaderinc"
#include "res://Shaders/Inc/Schlick.gdshaderinc"
uniform vec4 _BASE_COLOR : source_color = __BLUE;
uniform float _COSINE_PHI_POSITION_OF_BASE_COLOR : hint_range(0.0, 1.0) = __COSINE_30_DEG;
uniform bool _ENABLE_SHADING_SHIFT = false;
uniform float _SHADING_SHIFT : hint_range(0, 1.0) = 0.5;
void fragment() {
	vec3 normal = normalize(NORMAL);
	float cosineTheta = normal.x;
	float cosinePhi = normal.z;
	float maxShift = min(_COSINE_PHI_POSITION_OF_BASE_COLOR, abs(1.0 - _COSINE_PHI_POSITION_OF_BASE_COLOR));
	float cosinePhiPositionShifted = _COSINE_PHI_POSITION_OF_BASE_COLOR
		- float(_ENABLE_SHADING_SHIFT) * (cosineTheta * _SHADING_SHIFT * maxShift);
	cosinePhiPositionShifted = clamp(cosinePhiPositionShifted, 0.0, 1.0);
	float facingRatio = clamp(cosinePhi, 0.0, 1.0);
	ALBEDO = vec3(
		ModifiedSchlicksBias_Safe(cosinePhiPositionShifted, _BASE_COLOR.r, facingRatio),
		ModifiedSchlicksBias_Safe(cosinePhiPositionShifted, _BASE_COLOR.g, facingRatio),
		ModifiedSchlicksBias_Safe(cosinePhiPositionShifted, _BASE_COLOR.b, facingRatio));
}

let's say i have a spherical coordinate system using mathematics convention. a spherical coordinate is represented by (rho, theta, phi). in this problem, i am only dealing with the set of points where rho=1. then, i define a "shift" in the +z reference axis using a pair S = (theta, phi). S means that the Z axis has been moved by S.theta polar angle and S.phi azimuthal angle. Now, i want to compute the new coordinates in the shifted system for all cartesian xyz points. (any xyz should have rho=1 in both coordinate systems).

another requirement i have is to get the positive azimuth range for each polar angle in the shifted coordinate system such z>=0. for example, if the shift is (theta=45 deg, phi=45 deg), then the azimuth can go from 0 to 135 or 0 to 45 for some polar angles to keep z>=0. how to do this?

for all of this stuff, i don't actually care about the specific theta and phi angles. my shader just cares about cosine(theta) and cosine(phi) to compute a shading curve. can any simplifications or optimizations be done given this knowledge?

all this stuff is in the context of the gdshader that a pasted earlier. basically, i want to be able to shift the "bright pole" away from (0,0,1) by specifying a deltaTheta and deltaPhi. however, when i shift the bright pole, the darkness equator still needs to be the on the XY plane where Z=0. My plan to do this is to get the surface normal, figure out what cosine(phi) it belongs to, compute the cosine(theta), figure out the maximum cosine(theta) could be if it were to extend to the darkness equator, divide the cosine(theta) position by that maximum, and use that as the facing ratio as input into ModifiedSchlicksBias_Safe.

So explain all the math i need for this and what the end result gdshader should look like.

---

cylinder dimensions:
radius = 0.015625
0.0078125
depth = 1

---------

provide functions f(x) that do the following:

1. Generates a smooth (infinitely differentiable) curve between points P1 (0, a), P2 (c, d), and P3 (1, b).
2. Visits the points in this order: P1, P2, P3.
3. a and b are in [0, 1]
4. c and d are in (0, 1)
5. f's domain is [0, 1]
6. f's range is [0,1]
