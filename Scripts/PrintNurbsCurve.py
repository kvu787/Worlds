import bpy

def print_nurbs_control_points():
    # Get the active object
    obj = bpy.context.active_object

    # Check if the object exists and is a curve
    if not obj or obj.type != 'CURVE':
        print("Please select a NURBS Curve object.")
        return

    print(f"--- Control Points for: {obj.name} ---")

    # A curve object can contain multiple splines
    for i, spline in enumerate(obj.data.splines):
        # Check if the spline type is actually NURBS
        if spline.type == 'NURBS':
            print(f"Spline {i}:")
            
            # Iterate through the points
            for j, p in enumerate(spline.points):
                # p.co is a 4D vector (x, y, z, w)
                coords = p.co
                print(f"  Point {j}: x={coords[0]!r}, y={coords[1]!r}, z={coords[2]!r}, weight={coords[3]!r}")
        else:
            print(f"Spline {i} is not a NURBS curve (Type: {spline.type}).")

if __name__ == "__main__":
    print_nurbs_control_points()
