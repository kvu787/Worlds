import bpy

def point_to_string(point, fs='0.2f'):
    return f"(x = {point.co.x:{fs}}, y = {point.co.y:{fs}}, z = {point.co.z:{fs}}, w = {point.co.w:{fs}})"

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
                print()
                continue

            print(f"  >>> Spline/Patch {i}")
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

            print(f"    Knot Vector U = Computed by Blender based on the above parameters")
            print(f"    Knot Vector V = Computed by Blender based on the above parameters")
            print()

            print("    Control Points (Local Coordinates):")
            for i in range(points_u):
                print(f"      i = {i}")
                for j in range(points_v):
                    print(f"        j = {j}")
                    print(f"        {point_to_string(spline.points[i * points_v + j])}")
            print()


def main():
    print_nurbs_math()

if __name__ == "__main__":
    main()
