import bpy

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
