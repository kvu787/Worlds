import bpy

def calculate_knots(order, point_count, use_endpoint, use_bezier, use_cyclic):
    """
    Generates a knot vector based on Blender's NURBS logic.
    """
    # Standard relation: Knots = Points + Order
    total_knots = point_count + order

    # 1. HANDLE BEZIER (Piecewise Bezier Curve)
    # If the spline is set to Bezier, knots are fully clamped at every segment.
    if use_bezier:
        knots = []
        # Calculate how many segments we have based on points and order
        # Note: This is an approximation of Blender's internal Bezier conversion
        # Blender usually ensures points = (segments * (order - 1)) + 1 for proper Bezier
        if use_endpoint:
            # Simple clamping for the review scope
            knots = [0.0] * order
            remainder = total_knots - (2 * order)
            if remainder > 0:
                 knots.extend([1.0] * remainder) # Simplified placeholder
            knots.extend([1.0] * order)
            return knots

    # 2. HANDLE ENDPOINT (Clamped / Pinned)
    if use_endpoint and not use_cyclic:
        knots = [0.0] * order

        # The number of steps between the clamped ends
        num_middle_segments = point_count - order

        if num_middle_segments > 0:
            for i in range(1, num_middle_segments + 1):
                knots.append(float(i))
            last_val = float(num_middle_segments + 1)
        else:
            last_val = 1.0

        knots.extend([last_val] * order)
        return knots

    # 3. HANDLE CYCLIC / UNIFORM
    # For cyclic, the domain is often treated as uniform unbounded
    return [float(i) for i in range(total_knots)]

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

        for i, spline in enumerate(obj.data.splines):
            if spline.type != 'NURBS':
                print(f"  Skipping Spline {i} (Type: {spline.type} - Not NURBS)")
                continue

            print(f"  >>> Spline/Patch {i}")
            print()

            u_count = spline.point_count_u
            v_count = spline.point_count_v
            order_u = spline.order_u
            order_v = spline.order_v

            print(f"    Grid:  U={u_count} V={v_count}")
            print(f"    Order: U={order_u} V={order_v}")

            # Extract flags for clarity
            end_u, end_v = spline.use_endpoint_u, spline.use_endpoint_v
            bez_u, bez_v = spline.use_bezier_u, spline.use_bezier_v
            cyc_u, cyc_v = spline.use_cyclic_u, spline.use_cyclic_v

            print(f"    Flags:")
            print(f"      Endpoint: U={end_u} V={end_v}")
            print(f"      Bezier:   U={bez_u} V={bez_v}")
            print(f"      Cyclic:   U={cyc_u} V={cyc_v}")

            # Removed hasattr check as it is generally unreliable for raw knots in bpy
            knots_u = calculate_knots(order_u, u_count, end_u, bez_u, cyc_u)
            knots_v = calculate_knots(order_v, v_count, end_v, bez_v, cyc_v)

            print(f"    Knot Vector U: Size={len(knots_u)} {knots_u}")
            print(f"    Knot Vector V: Size={len(knots_v)} {knots_v}")
            print()

            print("    Control Points (Local Coordinates):")
            points = spline.points

            for v in range(v_count):
                row_str = f"      Row V={v}: "
                coords = []
                for u in range(u_count):
                    index = v * u_count + u
                    if index < len(points):
                        pt = points[index]
                        # pt.co is x,y,z,w (Homogeneous)
                        coords.append(f"[{pt.co.x:.2f}, {pt.co.y:.2f}, {pt.co.z:.2f}] w={pt.co.w:.2f}")

                # Print row compactly
                print(row_str)
                for c in coords:
                    print(f"        {c}")
        print()

def main():
    print_nurbs_math()

if __name__ == "__main__":
    main()
