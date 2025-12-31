#ifndef SCHLICK_INC
#define SCHLICK_INC

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
	if (c > d) {
		return 0.0;
	}

	if (isnan(t)) { return t; }
	if (isnan(a)) { return a; }
	if (isnan(b)) { return b; }
	if (isnan(c)) { return c; }
	if (isnan(d)) { return d; }

	t = clamp(t, 0.0, 1.0);
	a = clamp(a, 0.0, 1.0);
	b = clamp(b, c, d);
	c = clamp(c, 0.0, 1.0);
	d = clamp(d, 0.0, 1.0);

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

#endif
