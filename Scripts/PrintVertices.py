import bpy

# Get the active object
obj = bpy.context.active_object

if obj and obj.type == 'MESH':
    print(f"--- Full Precision Local Coordinates: {obj.name} ---")

    mesh = obj.data

    for v in mesh.vertices:
        # Use repr() for the most unambiguous representation of the float
        # or use '.20f' to force 20 decimal places
        print(f"Vertex {v.index}: X={repr(v.co.x)}, Y={repr(v.co.y)}, Z={repr(v.co.z)}")
else:
    print("Please select a mesh object.")
