import bpy
import math

def move_nurbs_control_point(old, new, epsilon):
    # Get the active object
    obj = bpy.context.active_object

    # Basic Validation
    if not obj:
        print("Error: No active object selected.")
        return
    if obj.type != 'SURFACE' and obj.type != 'CURVE':
        print(f"Error: Selected object is type '{obj.type}', expected 'SURFACE' or 'CURVE'.")
        return

    # Counter to track if we found anything
    points_moved = 0

    # Iterate through all splines in the surface (NURBS surfaces are collections of splines)
    for spline in obj.data.splines:
        # NURBS control points are stored in spline.points
        # Each point has a .co attribute (x, y, z, w)
        for point in spline.points:

            # Extract current XYZ (ignoring W for the position check)
            current_x, current_y, current_z = point.co.x, point.co.y, point.co.z

            # Check if the point matches the target old coordinates
            # We use math.isclose to handle floating point storage of integers
            if (math.isclose(current_x, old[0], abs_tol=epsilon) and
                math.isclose(current_y, old[1], abs_tol=epsilon) and
                math.isclose(current_z, old[2], abs_tol=epsilon)):

                # Update to new coordinates
                point.co.x = new[0]
                point.co.y = new[1]
                point.co.z = new[2]

                points_moved += 1
                print(f"Moved point from {old} to {new}")

    # Force an update of the geometry to reflect changes in the viewport
    # Toggling edit mode is often the most reliable way to refresh NURBS handles
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')

    if points_moved == 0:
        print("No matching control points found.")
    else:
        print(f"Success! Moved {points_moved} control point(s).")
'''
Inner ring
(1,1,1)
(2,1,1)
(2,2,1)
(1,2,1)

Corners
(0,0,0)
    (2,2,0)
    (1,2,0)
    (1,1,0)
    (2,1,0)
(3,0,0)
(3,3,0)
(0,3,0)

Sides
(1,0,0)
    (1,1,0)
    (2,1,0)
    (2,2,0)
    (1,2,0)
(2,0,0)
(3,1,0)
(3,2,0)
(2,3,0)
(1,3,0)
(0,2,0)
(0,1,0)
'''

# Run the function
move_nurbs_control_point(old=(2, 1, 1), new=(3, 3, 3), epsilon=0)
