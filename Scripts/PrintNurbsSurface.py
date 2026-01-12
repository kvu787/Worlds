import bpy

def compute_knot_vector(points_count, order, use_endpoint, use_cyclic):
    """
    Computes the knot vector for a NURBS dimension (U or V).
    Assumes use_bezier is False.
    """
    # Total number of knots in the vector
    knot_count = points_count + order
    
    knots = []

    if use_endpoint and not use_cyclic:
        # CLAMPED KNOT VECTOR
        # Used when 'Endpoint' is True (and not Cyclic).
        # Multiplicity of first and last knots equals the order.
        # The range is normalized to [0.0, 1.0].
        
        # Add 'order' number of 0.0s at the start
        knots.extend([0.0] * order)
        
        # Calculate internal knots
        # We need to distribute (points_count - order) knots evenly between 0 and 1
        internal_knots_count = points_count - order
        if internal_knots_count > 0:
            # The denominator is the number of spans formed by internal knots + 1
            # e.g., 1 internal knot creates 2 spans (0 -> 0.5 -> 1)
            denominator = internal_knots_count + 1
            for i in range(1, denominator):
                knots.append(i / denominator)
        
        # Add 'order' number of 1.0s at the end
        knots.extend([1.0] * order)

    else:
        # UNIFORM KNOT VECTOR
        # Used when 'Endpoint' is False (Unclamped) OR 'Cyclic' is True.
        # This is a simple sequence: 0.0, 1.0, 2.0, ...
        knots = [float(i) for i in range(knot_count)]
        
    return knots

def point_to_string(point):
    return f"(x = {point.co.x!r}, y = {point.co.y!r}, z = {point.co.z!r}, w = {point.co.w!r})"

def print_nurbs_math():
    selected_objects = bpy.context.selected_objects
    nurbs_surfaces = [obj for obj in selected_objects if obj.type == 'SURFACE']

    if not nurbs_surfaces:
        print("Error: No NURBS Surface objects are currently selected.")
        return

    print("=" * 80)
    print(f"PROCESSING {len(nurbs_surfaces)} SELECTED NURBS SURFACE(S)")
    print()

    for obj_index, obj in enumerate(nurbs_surfaces):
        print("-" * 40)
        print(f"OBJECT {obj_index + 1}/{len(nurbs_surfaces)}: {obj.name}")
        print()

        for spline_index, spline in enumerate(obj.data.splines):
            if spline.type != 'NURBS':
                print(f"  Skipping Spline {spline_index} (Type: {spline.type} - Not NURBS)")
                print()
                continue

            print(f"  >>> Spline/Patch {spline_index} NURBS Surface Definition")
            print()

            points_u = spline.point_count_u
            points_v = spline.point_count_v
            order_u = spline.order_u
            order_v = spline.order_v

            print(f"    Points Along U = {points_u}")
            print(f"    Points Along V = {points_v}")
            print(f"    Order U = {order_u}")
            print(f"    Order V = {order_v}")
            print()

            # Extract flags for clarity
            end_u, end_v = spline.use_endpoint_u, spline.use_endpoint_v
            bez_u, bez_v = spline.use_bezier_u, spline.use_bezier_v
            cyc_u, cyc_v = spline.use_cyclic_u, spline.use_cyclic_v

            print(f"    Blender Flags:")
            print(f"      Endpoint U = {end_u}")
            print(f"      Endpoint V = {end_v}")
            print(f"      Bezier U   = {bez_u}")
            print(f"      Bezier V   = {bez_v}")
            print(f"      Cyclic U   = {cyc_u}")
            print(f"      Cyclic V   = {cyc_v}")
            print()

            knots_u = None
            knots_v = None
            if bez_u or bez_v:
                knots_u = "Computed by Blender based on the above parameters"
                knots_v = knots_u
            else:
                knots_u = compute_knot_vector(points_u, order_u, end_u, cyc_u)
                knots_v = compute_knot_vector(points_v, order_v, end_v, cyc_v)
            print(f"    Knot Vector U = {knots_u}")
            print(f"    Knot Vector V = {knots_v}")
            print()

            print("    Control Points List (Local Coordinates):")
            for pt in spline.points:
                print(f"        {point_to_string(pt)}")
            print()

            print("    Control Points Grid (Local Coordinates):")
            for j in range(points_v):
                print(f"      j = {j}")
                for i in range(points_u):
                    # Blender stores control points in spline.points in V-major order
                    print(f"        i = {i} {point_to_string(spline.points[j * points_u + i])}")
            print()


def main():
    print_nurbs_math()

if __name__ == "__main__":
    main()
